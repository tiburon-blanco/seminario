"""Loaders para normalizar datos scrapeados desde Star Computación."""

import re

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from price_manager.scraper.items import StarComputacionItem


def limpiar_texto(valor: str) -> str:
  """Limpia espacios repetidos, saltos de línea y tabulaciones."""
  if valor is None:
    return ""

  texto = str(valor)
  texto = texto.replace("\xa0", " ")
  texto = re.sub(r"\s+", " ", texto)

  return texto.strip()


def limpiar_precio(valor: str) -> str:
  """Normaliza el texto de un precio."""
  texto = limpiar_texto(valor)

  return texto


class StarComputacionLoader(ItemLoader):
  """Loader para cargar y limpiar datos de Star Computación."""

  default_item_class = StarComputacionItem

  default_input_processor = MapCompose(limpiar_texto)
  default_output_processor = TakeFirst()

  producto_buscado_in = MapCompose(limpiar_texto)
  producto_buscado_out = TakeFirst()

  titulo_in = MapCompose(limpiar_texto)
  titulo_out = TakeFirst()

  precio_in = MapCompose(limpiar_precio)
  precio_out = TakeFirst()

  imagen_url_in = MapCompose(limpiar_texto)
  imagen_url_out = TakeFirst()

  formas_pago_in = MapCompose(limpiar_texto)
  formas_pago_out = Join(" | ")

  precio_forma_pago_in = MapCompose(limpiar_precio)
  precio_forma_pago_out = TakeFirst()

  descripcion_detallada_in = MapCompose(limpiar_texto)
  descripcion_detallada_out = Join(" ")

  url_in = MapCompose(limpiar_texto)
  url_out = TakeFirst()

  fuente_in = MapCompose(limpiar_texto)
  fuente_out = TakeFirst()