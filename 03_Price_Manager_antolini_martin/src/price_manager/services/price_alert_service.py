"""Servicio para comparar precios internos contra precios web y generar alertas."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from price_manager.repositories.repositories import RepositorioProducto
from price_manager.services.audit_service import auditar_accion


def _obtener_attr(objeto: Any, nombre: str, default: Any = None) -> Any:
  """Obtiene un atributo desde un objeto o diccionario."""
  if isinstance(objeto, dict):
    return objeto.get(nombre, default)

  return getattr(objeto, nombre, default)


def extraer_precio_numerico(valor: str | int | float | None) -> float | None:
  """Convierte un precio textual en número.

  Soporta formatos argentinos simples como:
  "$ 45.000", "$45.000,50", "45000", "45.000".
  """
  if valor is None:
    return None

  if isinstance(valor, (int, float)):
    return float(valor)

  texto = str(valor)
  coincidencias = re.findall(r"[\d\.,]+", texto)

  if not coincidencias:
    return None

  numero = coincidencias[0]

  if "," in numero:
    numero = numero.replace(".", "")
    numero = numero.replace(",", ".")
  else:
    partes = numero.split(".")

    if len(partes) > 1 and len(partes[-1]) == 3:
      numero = numero.replace(".", "")

  try:
    return float(numero)
  except ValueError:
    return None


def leer_jsonl(ruta: str | Path) -> list[dict[str, Any]]:
  """Lee un archivo JSON Lines y devuelve una lista de diccionarios."""
  ruta = Path(ruta)

  if not ruta.exists():
    return []

  resultados = []

  with ruta.open("r", encoding="utf-8") as archivo:
    for linea in archivo:
      if linea.strip():
        resultados.append(json.loads(linea))

  return resultados


def obtener_precio_interno_ars(
  producto: Any,
  cotizacion_usd: float = 1000.0,
) -> float | None:
  """Obtiene el precio interno del producto expresado en ARS.

  Si el producto está en USD, lo convierte usando cotizacion_usd.
  """
  precio = _obtener_attr(producto, "precio")

  if precio is None:
    precio_valor = _obtener_attr(producto, "precio_valor")
    moneda_nombre = _obtener_attr(producto, "moneda", "ARS")
  else:
    precio_valor = _obtener_attr(precio, "valor")
    moneda = _obtener_attr(precio, "moneda")
    moneda_nombre = _obtener_attr(moneda, "nombre", "ARS")

  if precio_valor is None:
    return None

  precio_ars = float(precio_valor)

  if str(moneda_nombre).upper() == "USD":
    precio_ars = precio_ars * cotizacion_usd

  return precio_ars


def construir_indice_productos_internos(
  productos_internos: list[Any] | None = None,
  cotizacion_usd: float = 1000.0,
) -> dict[str, dict[str, Any]]:
  """Construye un índice de productos internos por nombre normalizado."""
  if productos_internos is None:
    repositorio = RepositorioProducto()
    productos_internos = repositorio.leer_todos()

  indice = {}

  for producto in productos_internos:
    nombre = _obtener_attr(producto, "nombre")

    if not nombre:
      continue

    precio_interno_ars = obtener_precio_interno_ars(
      producto=producto,
      cotizacion_usd=cotizacion_usd,
    )

    if precio_interno_ars is None:
      continue

    clave = str(nombre).strip().lower()

    indice[clave] = {
      "producto_interno": nombre,
      "precio_interno_ars": precio_interno_ars,
    }

  return indice


def comparar_item_web(
  item_web: dict[str, Any],
  indice_productos: dict[str, dict[str, Any]],
  diferencia_maxima_porcentaje: float,
) -> dict[str, Any] | None:
  """Compara un item web contra el precio interno correspondiente."""
  producto_buscado = item_web.get("producto_buscado")

  if not producto_buscado:
    return None

  clave_producto = str(producto_buscado).strip().lower()
  producto_interno = indice_productos.get(clave_producto)

  if producto_interno is None:
    return None

  precio_interno = producto_interno["precio_interno_ars"]
  precio_web = extraer_precio_numerico(item_web.get("precio"))

  if precio_web is None or precio_interno == 0:
    return None

  diferencia_monto = precio_web - precio_interno
  diferencia_porcentaje = (diferencia_monto / precio_interno) * 100
  alerta = abs(diferencia_porcentaje) >= diferencia_maxima_porcentaje

  return {
    "producto_buscado": producto_buscado,
    "titulo_web": item_web.get("titulo", ""),
    "precio_interno_ars": round(precio_interno, 2),
    "precio_web_ars": round(precio_web, 2),
    "diferencia_monto": round(diferencia_monto, 2),
    "diferencia_porcentaje": round(diferencia_porcentaje, 2),
    "diferencia_maxima_permitida": diferencia_maxima_porcentaje,
    "alerta": "SI" if alerta else "NO",
    "url": item_web.get("url", ""),
    "imagen_url": item_web.get("imagen_url", ""),
    "formas_pago": item_web.get("formas_pago", ""),
    "precio_forma_pago": item_web.get("precio_forma_pago", ""),
    "descripcion_detallada": item_web.get("descripcion_detallada", ""),
    "fuente": item_web.get("fuente", ""),
  }

@auditar_accion("generar_alertas_precios")
def generar_alertas_precios(
  ruta_resultados_web: str | Path,
  ruta_alertas_csv: str | Path,
  diferencia_maxima_porcentaje: float,
  productos_internos: list[Any] | None = None,
  cotizacion_usd: float = 1000.0,
  solo_alertas: bool = True,
) -> list[dict[str, Any]]:
  """Genera un archivo CSV de alertas comparando precios internos y web.

  Args:
    ruta_resultados_web: Archivo JSONL generado por el scraper.
    ruta_alertas_csv: Ruta del CSV de alertas a generar.
    diferencia_maxima_porcentaje: Porcentaje máximo permitido.
    productos_internos: Lista opcional de productos internos.
    cotizacion_usd: Cotización usada si el precio interno está en USD.
    solo_alertas: Si True, guarda solo diferencias que superan el umbral.

  Returns:
    Lista de comparaciones o alertas generadas.
  """
  resultados_web = leer_jsonl(ruta_resultados_web)

  indice_productos = construir_indice_productos_internos(
    productos_internos=productos_internos,
    cotizacion_usd=cotizacion_usd,
  )

  comparaciones = []

  for item_web in resultados_web:
    comparacion = comparar_item_web(
      item_web=item_web,
      indice_productos=indice_productos,
      diferencia_maxima_porcentaje=diferencia_maxima_porcentaje,
    )

    if comparacion is None:
      continue

    if solo_alertas and comparacion["alerta"] != "SI":
      continue

    comparaciones.append(comparacion)

  ruta_alertas_csv = Path(ruta_alertas_csv)
  ruta_alertas_csv.parent.mkdir(parents=True, exist_ok=True)

  columnas = [
    "producto_buscado",
    "titulo_web",
    "precio_interno_ars",
    "precio_web_ars",
    "diferencia_monto",
    "diferencia_porcentaje",
    "diferencia_maxima_permitida",
    "alerta",
    "url",
    "imagen_url",
    "formas_pago",
    "precio_forma_pago",
    "descripcion_detallada",
    "fuente",
  ]

  with ruta_alertas_csv.open("w", newline="", encoding="utf-8") as archivo:
    writer = csv.DictWriter(archivo, fieldnames=columnas)
    writer.writeheader()

    for comparacion in comparaciones:
      writer.writerow(comparacion)

  return comparaciones

@auditar_accion("ejecutar_scraper_y_generar_alertas")
def ejecutar_scraper_y_generar_alertas(
  productos: list[str] | None = None,
  diferencia_maxima_porcentaje: float = 20.0,
  limite_por_busqueda: int = 10,
  scraper_output_path: str = "data/star_computacion_productos.jsonl",
  alertas_output_path: str = "data/alertas_precios.csv",
  cotizacion_usd: float = 1000.0,
) -> dict[str, Any]:
  """Ejecuta el scraper y genera el CSV de alertas.

  Esta función integra el Ejercicio 03 con el Ejercicio 04.
  """
  from price_manager.scraper.runner import ejecutar_scraper_star_computacion

  ruta_resultados = ejecutar_scraper_star_computacion(
    productos=productos,
    limite_por_busqueda=limite_por_busqueda,
    output_path=scraper_output_path,
  )

  alertas = generar_alertas_precios(
    ruta_resultados_web=ruta_resultados,
    ruta_alertas_csv=alertas_output_path,
    diferencia_maxima_porcentaje=diferencia_maxima_porcentaje,
    cotizacion_usd=cotizacion_usd,
    solo_alertas=True,
  )

  return {
    "ruta_resultados_web": Path(ruta_resultados),
    "ruta_alertas_csv": Path(alertas_output_path),
    "cantidad_alertas": len(alertas),
    "alertas": alertas,
  }