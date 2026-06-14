"""Spider para obtener precios de Star Computacion."""

from __future__ import annotations
import re
from html import unescape

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
  category_urls_by_keyword = {
        "notebook": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/notebooks-10/",
            "https://www.starcomputacion.com.ar/prods/computacin-1/lenovo-109/",
        ],
        "lenovo": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/notebooks-10/",
            "https://www.starcomputacion.com.ar/prods/computacin-1/lenovo-109/",
        ],
        "mouse": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/mouses-y-pads-23/",
        ],
        "logitech": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/mouses-y-pads-23/",
        ],
        "teclado": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/teclados-27/",
        ],
        "redragon": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/teclados-27/",
        ],
        "monitor": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/monitores-13/",
        ],
        "samsung": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/monitores-13/",
        ],
        "ssd": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/discos-36/",
        ],
        "kingston": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/discos-36/",
        ],
        "router": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/router-223/",
        ],
        "tp-link": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/router-223/",
        ],
        "impresora": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/impresoras-14/",
        ],
        "hp": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/impresoras-14/",
        ],
        "auriculares": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/auriculares-gamers-37/",
        ],
        "hyperx": [
            "https://www.starcomputacion.com.ar/prods/computacin-1/auriculares-gamers-37/",
        ],
        "hub": [
            "https://www.starcomputacion.com.ar/prods/electronica-2/hubs-y-adaptadores-267/",
        ],
        "usb": [
            "https://www.starcomputacion.com.ar/prods/electronica-2/hubs-y-adaptadores-267/",
        ],
    }

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
    self.urls_vistas = set()
    self.cantidad_por_producto = {}

  def obtener_urls_para_producto(self, producto: str) -> list[str]:
        """Obtiene URLs de busqueda y categorias asociadas al producto."""
        urls = [
            search_url.format(query=quote_plus(producto))
            for search_url in self.search_urls
        ]

        producto_normalizado = producto.lower()

        for palabra_clave, category_urls in self.category_urls_by_keyword.items():
            if palabra_clave in producto_normalizado:
                urls.extend(category_urls)

        urls_unicas = []

        for url in urls:
            if url not in urls_unicas:
                urls_unicas.append(url)

        return urls_unicas

  def generar_solicitudes_iniciales(self):
        """Genera solicitudes iniciales para cada producto propio."""
        if not self.productos:
            self.logger.warning("No se recibieron productos para buscar.")
            return

        for producto in self.productos:
            for url in self.obtener_urls_para_producto(producto):
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
  
  def producto_coincide_con_busqueda(
        self,
        producto_buscado: str,
        url: str,
    ) -> bool:
        """Valida que la URL del producto tenga relación con la búsqueda."""
        texto = url.lower()

        palabras = [
            palabra.lower()
            for palabra in producto_buscado.replace("-", " ").split()
            if len(palabra) >= 3
        ]

        return any(palabra in texto for palabra in palabras)

  def parse_resultados_busqueda(self, response):
        """Procesa una pagina de categoria o busqueda y obtiene productos."""
        producto_buscado = response.meta.get("producto_buscado")

        es_producto_actual = "/prod/" in response.url
        es_categoria_actual = "/prods/" in response.url

        if es_producto_actual and not es_categoria_actual:
            yield from self.parse_detalle_producto(response)
            return

        enlaces = []

        # 1) Buscar todos los href del HTML.
        enlaces.extend(response.css("a::attr(href)").getall())

        # 2) Buscar enlaces dentro del HTML crudo.
        html_normalizado = unescape(response.text)
        html_normalizado = html_normalizado.replace("\\/", "/")
        html_normalizado = html_normalizado.replace("\\u002F", "/")

        patrones = [
            r"https?://(?:www\.)?starcomputacion\.com\.ar/prod/[^\"'\s<>]+",
            r"/prod/[^\"'\s<>]+",
            r"prod/[^\"'\s<>]+",
        ]

        for patron in patrones:
            enlaces.extend(re.findall(patron, html_normalizado))

        enlaces_unicos = []
        cantidad_actual = self.cantidad_por_producto.get(producto_buscado, 0)

        for enlace in enlaces:
            url = response.urljoin(enlace)

            url = url.split("#")[0]
            url = url.split("?")[0]
            url = url.rstrip(".,);'\"")

            es_producto = "/prod/" in url
            es_categoria = "/prods/" in url

            if not es_producto or es_categoria:
                continue

            if not self.producto_coincide_con_busqueda(producto_buscado, url):
                continue

            if url in self.urls_vistas:
                continue

            if cantidad_actual >= self.limite_por_busqueda:
                break

            self.urls_vistas.add(url)
            enlaces_unicos.append(url)

            cantidad_actual += 1
            self.cantidad_por_producto[producto_buscado] = cantidad_actual

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
        producto_buscado = response.meta.get("producto_buscado")

        titulo = self.extraer_titulo_producto(response)
        precio = self.extraer_precio_producto(response)
        imagen_url = self.extraer_imagen_producto(response)
        formas_pago = self.extraer_formas_pago_limpias(response.text)
        precio_forma_pago = self.extraer_precio_forma_pago(precio)
        descripcion_detallada = self.extraer_descripcion_producto(
            response,
            titulo,
        )

        item = {
            "producto_buscado": producto_buscado,
            "titulo": titulo,
            "precio": precio,
            "imagen_url": imagen_url,
            "formas_pago": formas_pago,
            "precio_forma_pago": precio_forma_pago,
            "descripcion_detallada": descripcion_detallada,
            "url": response.url,
            "fuente": self.base_url,
        }

        yield item 

  def limpiar_texto(self, valor: str | None) -> str:
        """Limpia espacios y saltos de linea."""
        if not valor:
            return ""

        return " ".join(str(valor).split())

  def extraer_titulo_producto(self, response) -> str:
        """Extrae el titulo del producto."""
        selectores = [
            "h1::text",
            "h1 *::text",
            ".product-title::text",
            ".title::text",
            'meta[property="og:title"]::attr(content)',
        ]

        for selector in selectores:
            textos = response.css(selector).getall()

            for texto in textos:
                texto_limpio = self.limpiar_texto(texto)

                if texto_limpio and texto_limpio.upper() != "STAR":
                    return texto_limpio

        return self.titulo_desde_url(response.url)

  def extraer_precio_producto(self, response) -> str:
        """Extrae el precio evitando scripts."""
        textos = response.xpath(
            "//*[not(self::script) and not(self::style)]"
            "/text()[contains(., '$') or contains(., 'ARS')]"
        ).getall()

        for texto in textos:
            texto_limpio = self.limpiar_texto(texto)

            if not texto_limpio:
                continue

            if "resources =" in texto_limpio:
                continue

            if "this.addEvent" in texto_limpio:
                continue

            if len(texto_limpio) > 80:
                continue

            if re.search(r"\d", texto_limpio):
                return texto_limpio

        coincidencia = re.search(
            r"ARS\s*[0-9]+(?:[.,][0-9]+)?",
            response.text,
        )

        if coincidencia:
            return self.limpiar_texto(coincidencia.group(0))

        return ""

  def extraer_imagen_producto(self, response) -> str:
        """Extrae una imagen real del producto evitando el logo del sitio."""
        coincidencia = re.search(
            r'"img_1":"([^"]+)"',
            response.text,
        )

        if coincidencia:
            archivo = coincidencia.group(1)
            return f"https://www.starcomputacion.com.ar/files/products/{archivo}"

        imagenes = []
        imagenes.extend(
            response.css('meta[property="og:image"]::attr(content)').getall()
        )
        imagenes.extend(response.css("img::attr(src)").getall())
        imagenes.extend(response.css("img::attr(data-src)").getall())

        for imagen in imagenes:
            if not imagen:
                continue

            if "logo_top_star" in imagen:
                continue

            if "/products/" in imagen or "/files/" in imagen:
                return response.urljoin(imagen)

        return ""

  def extraer_formas_pago_limpias(self, html: str) -> str:
        """Extrae formas de pago limpias evitando scripts."""
        html_mayuscula = html.upper()
        formas = []

        if "6 CUOTAS" in html_mayuscula:
            formas.append("6 cuotas")

        if "12 CUOTAS" in html_mayuscula:
            formas.append("12 cuotas")

        if "TRANSFERENCIA" in html_mayuscula:
            formas.append("transferencia bancaria")

        if "MERCADO PAGO" in html_mayuscula or "MERPAGO" in html_mayuscula:
            formas.append("Mercado Pago")

        return " | ".join(formas)

  def extraer_precio_forma_pago(self, precio: str | None) -> str:
        """Calcula una referencia simple de precio por cuota."""
        if not precio:
            return ""

        numeros = re.sub(r"[^\d]", "", str(precio))

        if not numeros:
            return ""

        valor = float(numeros)
        cuota_6 = valor / 6

        return f"6 cuotas de ARS {cuota_6:.2f}"

  def extraer_descripcion_producto(self, response, titulo: str) -> str:
        """Extrae una descripcion valida del producto."""
        selectores = [
            'meta[name="description"]::attr(content)',
            'meta[property="og:description"]::attr(content)',
            ".description::text",
            ".descripcion::text",
        ]

        for selector in selectores:
            textos = response.css(selector).getall()

            for texto in textos:
                texto_limpio = self.limpiar_texto(texto)

                if not texto_limpio:
                    continue

                if texto_limpio.upper() == "STAR":
                    continue

                if "resources =" in texto_limpio:
                    continue

                if "this.addEvent" in texto_limpio:
                    continue

                return texto_limpio

        return titulo

  def titulo_desde_url(self, url: str) -> str:
    """Genera un titulo legible desde el slug de la URL."""
    slug = url.rstrip("/").split("/")[-1]
    partes = slug.split("-")

    if partes and partes[-1].isdigit():
        partes = partes[:-1]

    return " ".join(partes).title()


  def extraer_imagen_producto(self, response) -> str:
    """Extrae una imagen de producto evitando el logo del sitio."""
    imagenes = response.css("img::attr(src)").getall()
    imagenes.extend(response.css("img::attr(data-src)").getall())

    for imagen in imagenes:
        if not imagen:
            continue

        if "logo_top_star" in imagen:
            continue

        if "/products/" in imagen or "/files/" in imagen:
            return response.urljoin(imagen)

    return ""


  def extraer_formas_pago_limpias(self, html: str) -> str:
    """Extrae formas de pago simples evitando scripts completos."""
    html_mayuscula = html.upper()
    formas = []

    if "CUOTA" in html_mayuscula or "CUOTAS" in html_mayuscula:
        formas.append("cuotas")

    if "TRANSFERENCIA" in html_mayuscula:
        formas.append("transferencia")

    if "TARJETA" in html_mayuscula:
        formas.append("tarjeta")

    return " | ".join(formas)


  def extraer_precio_forma_pago(self, precio: str | None) -> str:
    """Calcula una referencia simple de pago en cuotas."""
    if not precio:
        return ""

    numeros = re.sub(r"[^\d]", "", str(precio))

    if not numeros:
        return ""

    valor = float(numeros)
    cuota_6 = valor / 6

    return f"6 cuotas de ARS {cuota_6:.2f}"