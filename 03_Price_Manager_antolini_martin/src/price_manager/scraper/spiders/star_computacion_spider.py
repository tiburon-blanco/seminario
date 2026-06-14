"""Spider para obtener precios de Star Computacion."""

from urllib.parse import quote_plus

import scrapy

from price_manager.scraper.loaders import StarComputacionLoader


class StarComputacionSpider(scrapy.Spider):
    """Spider de Scrapy para consultar productos en Star Computacion."""

    name = "star_computacion"
    allowed_domains = ["starcomputacion.com.ar"]

    base_url = "https://www.starcomputacion.com.ar"

    search_urls = [
        "https://www.starcomputacion.com.ar/search/?q={query}",
        "https://www.starcomputacion.com.ar/?s={query}",
    ]

    def __init__(
        self,
        productos=None,
        limite_por_busqueda=10,
        output_path=None,
        *args,
        **kwargs,
    ):
        """Inicializa el spider con los productos a buscar."""
        super().__init__(*args, **kwargs)

        if productos is None:
            self.productos = []
        elif isinstance(productos, str):
            self.productos = [productos]
        else:
            self.productos = list(productos)

        self.limite_por_busqueda = int(limite_por_busqueda)
        self.output_path = output_path

    def start_requests(self):
        """Genera solicitudes de busqueda para cada producto."""
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

    def parse_resultados_busqueda(self, response):
        """Procesa una pagina de resultados y obtiene enlaces de productos."""
        producto_buscado = response.meta.get("producto_buscado")

        enlaces = []

        selectores_enlaces = [
            'a[href*="/prod/"]::attr(href)',
            'a[href*="/productos/"]::attr(href)',
            'a[href*="/producto/"]::attr(href)',
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
                or "/productos/" in url
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

        loader.add_value("producto_buscado", response.meta.get("producto_buscado"))

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

        loader.add_css("imagen_url", 'meta[property="og:image"]::attr(content)')
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