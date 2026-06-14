"""Runner para ejecutar el scraper de Star Computación."""

from __future__ import annotations

import json
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from price_manager.services.audit_service import auditar_accion

from price_manager.database.connection import ConexionDB
from price_manager.repositories.repositories import RepositorioProducto
from price_manager.scraper.spiders.star_computacion_spider import (
  StarComputacionSpider,
)

@auditar_accion("obtener_nombres_productos_propios")
def obtener_nombres_productos_propios() -> list[str]:
    """Obtiene los nombres de productos propios para usar en el scraper.

    Primero intenta obtener productos desde la base de datos.
    Si la base no devuelve resultados, utiliza el archivo productos.csv
    de la precarga del proyecto.
    """
    productos: list[str] = []

    try:
        from price_manager.database.connection import ConexionDB
        from price_manager.models.models import ProductoModel

        conexion = ConexionDB()
        session = conexion.obtener_sesion()

        try:
            registros = session.query(ProductoModel).all()

            for registro in registros:
                nombre = getattr(registro, "nombre", None)

                if nombre:
                    productos.append(str(nombre).strip())
        finally:
            session.close()

    except Exception:
        productos = []

    productos = [
        producto
        for producto in productos
        if producto
    ]

    if productos:
        return productos

    # Fallback: productos propios desde productos.csv
    import csv
    from pathlib import Path

    ruta_csv = (
        Path(__file__).resolve().parents[1]
        / "migrations"
        / "csv"
        / "productos.csv"
    )

    if not ruta_csv.exists():
        return []

    contenido = ruta_csv.read_text(encoding="utf-8-sig")
    primera_linea = contenido.splitlines()[0]

    delimitador = ";" if primera_linea.count(";") > primera_linea.count(",") else ","

    lector = csv.DictReader(
        contenido.splitlines(),
        delimiter=delimitador,
    )

    columnas = lector.fieldnames or []

    posibles_columnas_nombre = [
        "nombre",
        "nombre_producto",
        "producto",
        "descripcion",
        "titulo",
    ]

    columna_nombre = None

    for columna in posibles_columnas_nombre:
        if columna in columnas:
            columna_nombre = columna
            break

    if columna_nombre is None:
        return []

    productos_csv = [
        fila[columna_nombre].strip()
        for fila in lector
        if fila.get(columna_nombre) and fila[columna_nombre].strip()
    ]

    return productos_csv

@auditar_accion("ejecutar_scraper_star_computacion")
def ejecutar_scraper_star_computacion(
  productos: list[str] | None = None,
  limite_por_busqueda: int = 10,
  output_path: str = "data/star_computacion_productos.jsonl",
) -> Path:
  """Ejecuta StarComputacionSpider para productos propios.

  Args:
    productos: Lista opcional de productos. Si no se informa, se obtienen
      desde la base de datos del sistema.
    limite_por_busqueda: Cantidad máxima de resultados por búsqueda.
    output_path: Ruta del archivo JSONL donde se guardan los resultados.

  Returns:
    Ruta del archivo de salida generado.
  """
  if productos is None:
    productos = obtener_nombres_productos_propios()

  productos_param = "|".join(productos)

  settings = get_project_settings()
  settings.setmodule("price_manager.scraper.settings")

  process = CrawlerProcess(settings)

  process.crawl(
    StarComputacionSpider,
    productos=productos_param,
    limite_por_busqueda=limite_por_busqueda,
    output_path=output_path,
  )

  process.start()

  return Path(output_path)


def leer_resultados_jsonl(ruta: str | Path) -> list[dict]:
  """Lee resultados generados por el pipeline JSON Lines."""
  ruta = Path(ruta)

  if not ruta.exists():
    return []

  resultados = []

  with ruta.open("r", encoding="utf-8") as archivo:
    for linea in archivo:
      if linea.strip():
        resultados.append(json.loads(linea))

  return resultados