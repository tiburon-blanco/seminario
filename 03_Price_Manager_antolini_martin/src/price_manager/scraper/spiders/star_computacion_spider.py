"""Spider para obtener precios de Star Computacion."""

from __future__ import annotations

from urllib.parse import quote_plus

import scrapy

from price_manager.scraper.loaders import StarComputacionLoader

class StarComputacionSpider(scrapy.Spider):
  """Spider de Scrapy para consultar productos en Star Computacion."""

  name = "star_computacion"
  allowed_domains = [
    "starcomputacion.com.ar",
    "www.starcomputacion.com.ar",
]

  base_url = "https://www.starcomputacion.com.ar"

  search_urls = [
    "https://www.starcomputacion.com.ar/search/?q={query}",
    "https://www.starcomputacion.com.ar/?s={query}",
    "https://www.starcomputacion.com.ar/buscar/{query}",
]

  def __init__(
      self,
      productos=None,
      limite_por_busqueda=10,
      output_path=None,
      *args,
      **kwargs,
  ):
    """Inicializa el spider con los productos propios a buscar."""
    super().__init__(*args, **kwargs)

    if productos is None:
        self.productos = []
    elif isinstance(productos, str):
        self.productos = [
            producto.strip()
            for producto in productos.split("|")
            if producto.strip()
        ]
    else:
        self.productos = [
            str(producto).strip()
            for producto in productos
            if str(producto).strip()
        ]

    self.limite_por_busqueda = int(limite_por_busqueda)
    self.output_path = output_path

  def generar_solicitudes_iniciales(self):
          """Genera solicitudes iniciales para cada producto propio."""
          if not self.productos:
              self.logger.warning("No se recibieron productos para buscar.")
              return

          for producto in self.productos:
              for search_url in self.search_urls:
                  url = search_url.format(query=quote_plus(producto))

                  yield scrapy.Request(
                      url=url,
                      callback=self.parse_resultados_busqueda,
                      meta={
                          "producto_buscado": producto,
                      },
                      dont_filter=True,
                )

  async def start(self):
        """Metodo inicial compatible con Scrapy 2.13 o superior."""
        for request in self.generar_solicitudes_iniciales():
            yield request

  def start_requests(self):
        """Metodo inicial compatible con versiones anteriores de Scrapy."""
        yield from self.generar_solicitudes_iniciales()


  def parse_resultados_busqueda(self, response):
    """Procesa resultados de busqueda y obtiene enlaces de productos."""
    producto_buscado = response.meta.get("producto_buscado")

    # Si la busqueda redirige directamente a un producto, se procesa.
    es_producto_actual = (
        "/prod/" in response.url
        or "/producto/" in response.url
    )
    es_categoria_actual = "/prods/" in response.url

    if es_producto_actual and not es_categoria_actual:
        yield from self.parse_detalle_producto(response)
        return

    enlaces = []

    selectores_enlaces = [
        'a[href*="/prod/"]::attr(href)',
        'a[href*="/producto/"]::attr(href)',
        'a[href*="/productos/"]::attr(href)',
    ]

    for selector in selectores_enlaces:
        enlaces.extend(response.css(selector).getall())

    if not enlaces:
        enlaces = response.css("a::attr(href)").re(r".*/prod/.*")

    enlaces_unicos = []

    for enlace in enlaces:
        url = response.urljoin(enlace)

        es_producto = (
            "/prod/" in url
            or "/producto/" in url
        )
        es_categoria = "/prods/" in url

        if not es_producto or es_categoria:
            continue

        if url not in enlaces_unicos:
            enlaces_unicos.append(url)

        if len(enlaces_unicos) >= self.limite_por_busqueda:
            break

    if not enlaces_unicos:
        self.logger.warning(
            "No se encontraron productos para la busqueda: %s",
            producto_buscado,
        )

    for url in enlaces_unicos:
        yield scrapy.Request(
            url=url,
            callback=self.parse_detalle_producto,
            meta={
                "producto_buscado": producto_buscado,
            },
            dont_filter=True,
        )

  def parse_detalle_producto(self, response):
    """Extrae los datos de detalle de un producto."""
    loader = StarComputacionLoader(response=response)

    loader.add_value(
        "producto_buscado",
        response.meta.get("producto_buscado"),
    )

    loader.add_css("titulo", "h1::text")
    loader.add_css("titulo", "h1 *::text")
    loader.add_css("titulo", ".product-title::text")
    loader.add_css("titulo", ".title::text")
    loader.add_css("titulo", 'meta[property="og:title"]::attr(content)')

    loader.add_css("precio", ".price::text")
    loader.add_css("precio", ".price *::text")
    loader.add_css("precio", ".precio::text")
    loader.add_css("precio", ".precio *::text")
    loader.add_xpath("precio", "//*[contains(text(), '$')]/text()")

    loader.add_css(
        "imagen_url",
        'meta[property="og:image"]::attr(content)',
    )
    loader.add_css("imagen_url", "img::attr(src)")
    loader.add_css("imagen_url", "img::attr(data-src)")

    loader.add_css("formas_pago", ".payment::text")
    loader.add_css("formas_pago", ".payment *::text")
    loader.add_css("formas_pago", ".cuotas::text")
    loader.add_css("formas_pago", ".cuotas *::text")
    loader.add_xpath(
        "formas_pago",
        "//*[contains(translate(text(), 'CUOTAS', 'cuotas'), 'cuotas')]/text()",
    )

    loader.add_css("precio_forma_pago", ".payment::text")
    loader.add_css("precio_forma_pago", ".payment *::text")
    loader.add_css("precio_forma_pago", ".cuotas::text")
    loader.add_css("precio_forma_pago", ".cuotas *::text")
    loader.add_xpath(
        "precio_forma_pago",
        "//*[contains(text(), '$')]/text()",
    )

    loader.add_css("descripcion_detallada", ".description::text")
    loader.add_css("descripcion_detallada", ".description *::text")
    loader.add_css("descripcion_detallada", ".descripcion::text")
    loader.add_css("descripcion_detallada", ".descripcion *::text")
    loader.add_css(
        "descripcion_detallada",
        'meta[name="description"]::attr(content)',
    )
    loader.add_css(
        "descripcion_detallada",
        'meta[property="og:description"]::attr(content)',
    )

    loader.add_value("url", response.url)
    loader.add_value("fuente", self.base_url)

    yield loader.load_item()



    """Extrae los datos solicitados desde el detalle del producto."""
    loader = StarComputacionLoader(response=response)

    loader.add_value("producto_buscado", response.meta["producto_buscado"])
    loader.add_value("url", response.url)
    loader.add_value("fuente", "Star Computación")

    # Título del producto.
    loader.add_css("titulo", "h1::text")
    loader.add_css("titulo", 'meta[property="og:title"]::attr(content)')
    loader.add_css("titulo", ".product-name::text")
    loader.add_css("titulo", ".js-product-name::text")
    loader.add_css("titulo", '[class*="title"]::text')

    # Precio.
    loader.add_css("precio", ".price::text")
    loader.add_xpath("precio", "//*[contains(text(), '$')]/text()")
    loader.add_css("precio", ".js-price-display::text")
    loader.add_css("precio", '[class*="price"]::text')
    loader.add_css("precio", '[class*="precio"]::text')
    # Imagen.
    loader.add_css("imagen_url", "img::attr(src)")
    loader.add_css("imagen_url", 'meta[property="og:image"]::attr(content)')
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
    loader.add_css(
      "descripcion_detallada",
      'meta[name="description"]::attr(content)',
    )
    loader.add_css(
      "descripcion_detallada",
      'meta[property="og:description"]::attr(content)',
    )

    yield loader.load_item()