"""Pipelines para validar, depurar y persistir resultados del scraper."""

import json
from pathlib import Path

from scrapy.exceptions import DropItem


class StarComputacionValidationPipeline:
  """Valida que el item tenga los datos mínimos requeridos."""

  def process_item(self, item, spider):
    """Procesa y valida un item scrapeado."""
    if not item.get("producto_buscado"):
      raise DropItem("Item descartado: falta producto_buscado.")

    if not item.get("url"):
      raise DropItem("Item descartado: falta url.")

    if not item.get("precio"):
      spider.logger.warning(
        "Item sin precio detectado para producto: %s",
        item.get("producto_buscado"),
      )

    return item


class StarComputacionDuplicatesPipeline:
  """Evita guardar resultados duplicados usando la URL como clave."""

  def __init__(self):
    """Inicializa el conjunto de URLs vistas."""
    self.urls_vistas = set()

  def process_item(self, item, spider):
    """Descarta items duplicados por URL."""
    url = item.get("url")

    if url in self.urls_vistas:
      raise DropItem(f"Item duplicado descartado: {url}")

    self.urls_vistas.add(url)

    return item


class StarComputacionJsonLinesPipeline:
  """Guarda los resultados del scraper en un archivo JSON Lines."""

  def open_spider(self, spider):
    """Abre el archivo de salida al iniciar el spider."""
    output_path = getattr(
      spider,
      "output_path",
      "data/star_computacion_productos.jsonl",
    )

    self.ruta_salida = Path(output_path)
    self.ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    self.archivo = self.ruta_salida.open(
      mode="w",
      encoding="utf-8",
    )

  def close_spider(self, spider):
    """Cierra el archivo de salida al finalizar el spider."""
    if hasattr(self, "archivo"):
      self.archivo.close()

  def process_item(self, item, spider):
    """Escribe cada item como una línea JSON."""
    linea = json.dumps(
      dict(item),
      ensure_ascii=False,
    )

    self.archivo.write(linea + "\n")

    return item