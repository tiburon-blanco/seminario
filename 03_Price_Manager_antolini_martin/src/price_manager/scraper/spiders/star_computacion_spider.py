"""Spider para obtener datos de productos desde Star Computación."""

from __future__ import annotations

from unittest import loader
from urllib.parse import quote_plus

import scrapy

from price_manager.scraper.loaders import StarComputacionLoader


class StarComputacionSpider(scrapy.Spider):
  """Spider de Star Computación limitado a productos propios."""

  name = "star_computacion"
  allowed_domains = ["starcomputacion.com.ar"]

  base_url = "https://www.starcomputacion.com.ar"
  search_url = "https://www.starcomputacion.com.ar/search/?q={query}"

  def __init__(
    self,
    productos: str | None = None,
    limite_por_busqueda: int = 10,
    output_path: str = "data/star_computacion_productos.jsonl",
    *args,
    **kwargs,
  ):
    """Inicializa el spider.

    Args:
      productos: Lista de productos separados por pipe. Ejemplo:
        "Teclado|Mouse|Monitor".
      limite_por_busqueda: Cantidad máxima de resultados por búsqueda.
      output_path: Ruta de salida para el pipeline JSONL.
    """
    super().__init__(*args, **kwargs)

    if productos is None:
      self.productos = []
    else:
      self.productos = [
        producto.strip()
        for producto in productos.split("|")
        if producto.strip()
      ]

    self.limite_por_busqueda = int(limite_por_busqueda)
    self.output_path = output_path

  def start_requests(self):
    """Genera las solicitudes de búsqueda para productos propios."""
    if not self.productos:
      self.logger.warning("No se recibieron productos para buscar.")
      return

    for producto in self.productos:
      url = self.search_url.format(query=quote_plus(producto))

      yield scrapy.Request(
        url=url,
        callback=self.parse_resultados_busqueda,
        meta={
          "producto_buscado": producto,
        },
      )

  def parse_resultados_busqueda(self, response):
    """Procesa los resultados de búsqueda y toma hasta 10 enlaces."""
    producto_buscado = response.meta["producto_buscado"]

    enlaces = response.css('a[href*="/productos/"]::attr(href)').getall()

    if not enlaces:
      enlaces = response.css('a[href*="/producto/"]::attr(href)').getall()

    if not enlaces:
      enlaces = response.css("a::attr(href)").re(r".*producto.*")

    enlaces_unicos = []

    for enlace in enlaces:
      url = response.urljoin(enlace)

      if url not in enlaces_unicos:
        enlaces_unicos.append(url)

      if len(enlaces_unicos) >= self.limite_por_busqueda:
        break

    if not enlaces_unicos:
      self.logger.warning(
        "No se encontraron resultados para: %s",
        producto_buscado,
      )

    for url in enlaces_unicos:
      yield scrapy.Request(
        url=url,
        callback=self.parse_detalle_producto,
        meta={
          "producto_buscado": producto_buscado,
        },
      )

  def parse_detalle_producto(self, response):
    """Extrae los datos solicitados desde el detalle del producto."""
    loader = StarComputacionLoader(response=response)

    loader.add_value("producto_buscado", response.meta["producto_buscado"])
    loader.add_value("url", response.url)
    loader.add_value("fuente", "Star Computación")

    # Título del producto.
    loader.add_css("titulo", "h1::text")
    loader.add_css("titulo", ".product-name::text")
    loader.add_css("titulo", ".js-product-name::text")
    loader.add_css("titulo", '[class*="title"]::text')

    # Precio.
    loader.add_css("precio", ".price::text")
    loader.add_css("precio", ".js-price-display::text")
    loader.add_css("precio", '[class*="price"]::text')
    loader.add_css("precio", '[class*="precio"]::text')
    # Imagen.
    loader.add_css("imagen_url", "img::attr(src)")
    loader.add_css("imagen_url", "img::attr(data-src)")
    loader.add_css("imagen_url", "img::attr(data-original)")

    # Formas de pago.
    loader.add_css("formas_pago", '[class*="payment"] *::text')
    loader.add_css("formas_pago", '[class*="pago"] *::text')
    loader.add_css("formas_pago", '[class*="cuota"] *::text')
    loader.add_css("formas_pago", '[class*="installment"] *::text')

    # Precio por forma de pago o cuotas.
    loader.add_css("precio_forma_pago", '[class*="installment"]::text')
    loader.add_css("precio_forma_pago", '[class*="cuota"]::text')
    loader.add_css("precio_forma_pago", '[class*="payment"]::text')
    loader.add_css("precio_forma_pago", '[class*="pago"]::text')

    # Descripción detallada.
    loader.add_css("descripcion_detallada", ".description *::text")
    loader.add_css("descripcion_detallada", ".product-description *::text")
    loader.add_css("descripcion_detallada", '[class*="description"] *::text')
    loader.add_css("descripcion_detallada", '[class*="descripcion"] *::text')
    loader.add_css("descripcion_detallada", ".tab-content *::text")

    yield loader.load_item()