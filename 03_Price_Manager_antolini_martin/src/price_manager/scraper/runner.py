"""Runner para ejecutar el scraper de Star Computación."""

from __future__ import annotations

import json
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from price_manager.database.connection import ConexionDB
from price_manager.repositories.repositories import RepositorioProducto
from price_manager.scraper.spiders.star_computacion_spider import (
  StarComputacionSpider,
)


def obtener_nombres_productos_propios() -> list[str]:
  """Obtiene los nombres de productos propios desde la base de datos."""
  ConexionDB().crear_tablas()

  repositorio = RepositorioProducto()
  productos = repositorio.leer_todos()

  return [
    producto.nombre
    for producto in productos
    if getattr(producto, "nombre", None)
  ]


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