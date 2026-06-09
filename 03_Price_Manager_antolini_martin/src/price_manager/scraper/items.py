"""Items del scraper de Star Computación."""

import scrapy


class StarComputacionItem(scrapy.Item):
  """Item con los datos extraídos desde Star Computación."""

  producto_buscado = scrapy.Field()
  titulo = scrapy.Field()
  precio = scrapy.Field()
  imagen_url = scrapy.Field()
  formas_pago = scrapy.Field()
  precio_forma_pago = scrapy.Field()
  descripcion_detallada = scrapy.Field()
  url = scrapy.Field()
  fuente = scrapy.Field()