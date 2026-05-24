"""Funciones de precarga de datos iniciales y lectura desde archivos CSV."""

import os
import csv
import datetime
from datetime import date

from price_manager.entities.entities import (
    Categoria,
    CotizacionDolar,
    Moneda,
    Precio,
    Producto,
    Proveedor,
    Stock,
    TipoCotizacion,
)

from price_manager.repositories.repositories import (
    RepositorioCategoria,
    RepositorioCotizacionDolar,
    RepositorioMoneda,
    RepositorioProducto,
    RepositorioProveedor,
    RepositorioStock,
    RepositorioTipoCotizacion,
)


# ============================================================
# DATOS INICIALES PARA GENERACIÓN DE SQL Y CSV
# ============================================================

categorias_iniciales = [
    Categoria(1, "Perifericos"),
    Categoria(2, "Hardware"),
    Categoria(3, "Almacenamiento"),
    Categoria(4, "Monitores"),
    Categoria(5, "Software"),
]


proveedores_iniciales = [
    Proveedor(1, "TechCorp", "ventas@techcorp.com"),
    Proveedor(2, "GlobalSupplies", "info@globalsupplies.net"),
    Proveedor(3, "ElectroMega", "contacto@electromega.arg"),
]


monedas_iniciales = [
    Moneda(1, "ARS"),
    Moneda(2, "USD"),
    Moneda(3, "EUR"),
]


tipos_cotizacion_iniciales = [
    TipoCotizacion(1, "Oficial"),
    TipoCotizacion(2, "Blue"),
    TipoCotizacion(3, "Tarjeta"),
]


productos_iniciales = [
    Producto(
        1,
        "Teclado Mecánico",
        "Teclado gamer RGB",
        Precio(
            15000.0,
            monedas_iniciales[0],
            date(2023, 10, 26),
        ),
        categorias_iniciales[0],
        proveedores_iniciales[0],
    ),
    Producto(
        2,
        "Mouse Óptico",
        "Mouse ergonómico 16000 DPI",
        Precio(
            8000.0,
            monedas_iniciales[0],
            date(2023, 10, 26),
        ),
        categorias_iniciales[0],
        proveedores_iniciales[0],
    ),
    Producto(
        3,
        "Monitor 27 pulgadas",
        "Monitor gaming 144Hz",
        Precio(
            120.0,
            monedas_iniciales[1],
            date(2023, 10, 26),
        ),
        categorias_iniciales[3],
        proveedores_iniciales[1],
    ),
    Producto(
        4,
        "SSD 1TB NVMe",
        "Unidad de estado sólido de alta velocidad",
        Precio(
            75.0,
            monedas_iniciales[1],
            date(2023, 10, 26),
        ),
        categorias_iniciales[2],
        proveedores_iniciales[1],
    ),
    Producto(
        5,
        "Procesador Intel i7",
        "CPU de última generación",
        Precio(
            350.0,
            monedas_iniciales[1],
            date(2023, 10, 26),
        ),
        categorias_iniciales[1],
        proveedores_iniciales[2],
    ),
]


# ============================================================
# STOCK INICIAL
# ============================================================
# Lista plana para generación de stock.csv.
# Esta lista evita problemas al importar el módulo y permite generar
# correctamente el archivo CSV de stock para las migraciones.

stock_inicial_csv = [
    {"producto_id": 1, "cantidad": 50},
    {"producto_id": 2, "cantidad": 120},
    {"producto_id": 3, "cantidad": 30},
    {"producto_id": 4, "cantidad": 80},
    {"producto_id": 5, "cantidad": 40},
]

# Alias de compatibilidad.
# Se evita instanciar Stock en la carga inicial para no romper el import
# si cambia la firma de la entidad Stock.
stock_inicial = stock_inicial_csv


cotizaciones_dolar_iniciales = [
    CotizacionDolar(
        350.0,
        fecha=date(2023, 10, 25),
        tipo=tipos_cotizacion_iniciales[0],
    ),
    CotizacionDolar(
        900.0,
        fecha=date(2023, 10, 25),
        tipo=tipos_cotizacion_iniciales[1],
    ),
    CotizacionDolar(
        700.0,
        fecha=date(2023, 10, 25),
        tipo=tipos_cotizacion_iniciales[2],
    ),
    CotizacionDolar(
        350.5,
        fecha=date(2023, 10, 26),
        tipo=tipos_cotizacion_iniciales[0],
    ),
    CotizacionDolar(
        910.0,
        fecha=date(2023, 10, 26),
        tipo=tipos_cotizacion_iniciales[1],
    ),
    CotizacionDolar(
        710.0,
        fecha=date(2023, 10, 26),
        tipo=tipos_cotizacion_iniciales[2],
    ),
]


# ============================================================
# FUNCIONES DE PRECARGA DESDE CSV
# ============================================================

def _obtener_ruta_csv(base_path: str | None = None) -> str:
    """Devuelve la ruta base donde se encuentran los archivos CSV."""
    if base_path is not None:
        return base_path

    ruta_actual = os.path.dirname(__file__)
    return os.path.normpath(
        os.path.join(ruta_actual, "..", "migrations", "csv")
    )


def _leer_csv(
    nombre_archivo: str,
    base_path: str | None = None,
) -> list[dict[str, str]]:
    """Lee un archivo CSV y devuelve una lista de diccionarios."""
    ruta_csv = _obtener_ruta_csv(base_path)
    ruta_archivo = os.path.join(ruta_csv, nombre_archivo)

    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


def precargar_datos(
    repo_categoria: RepositorioCategoria,
    repo_proveedor: RepositorioProveedor,
    repo_moneda: RepositorioMoneda,
    repo_tipo_cotizacion: RepositorioTipoCotizacion,
    repo_producto: RepositorioProducto,
    repo_stock: RepositorioStock,
    repo_cotizacion: RepositorioCotizacionDolar,
    base_path: str | None = None,
) -> None:
    """Precarga datos desde los archivos CSV hacia los repositorios."""

    for fila in _leer_csv("categorias.csv", base_path):
        try:
            categoria = Categoria(
                int(fila["id"]),
                fila["nombre"],
            )
            repo_categoria.crear(categoria)
        except ValueError:
            pass

    for fila in _leer_csv("proveedores.csv", base_path):
        try:
            proveedor = Proveedor(
                int(fila["id"]),
                fila["nombre"],
                fila["contacto"],
            )
            repo_proveedor.crear(proveedor)
        except ValueError:
            pass

    for fila in _leer_csv("monedas.csv", base_path):
        try:
            moneda = Moneda(
                int(fila["id"]),
                fila["nombre"],
            )
            repo_moneda.crear(moneda)
        except ValueError:
            pass

    for fila in _leer_csv("tipos_cotizacion.csv", base_path):
        try:
            tipo = TipoCotizacion(
                int(fila["id"]),
                fila["nombre"],
            )
            repo_tipo_cotizacion.crear(tipo)
        except ValueError:
            pass

    for fila in _leer_csv("productos.csv", base_path):
        try:
            moneda = repo_moneda.leer_por_id(int(fila["moneda_id"]))
            categoria = repo_categoria.leer_por_id(int(fila["categoria_id"]))
            proveedor = repo_proveedor.leer_por_id(int(fila["proveedor_id"]))

            if moneda is None:
                raise ValueError("No existe la moneda asociada al producto.")

            if categoria is None:
                raise ValueError("No existe la categoría asociada al producto.")

            if proveedor is None:
                raise ValueError("No existe el proveedor asociado al producto.")

            fecha_precio = datetime.date.fromisoformat(fila["precio_fecha"])

            precio = Precio(
                float(fila["precio_valor"]),
                moneda,
                fecha_precio,
            )

            producto = Producto(
                int(fila["id"]),
                fila["nombre"],
                fila["descripcion"],
                precio,
                categoria,
                proveedor,
            )

            repo_producto.crear(producto)

        except ValueError:
            pass

    for fila in _leer_csv("stock.csv", base_path):
        try:
            producto = repo_producto.leer_por_id(int(fila["producto_id"]))

            if producto is None:
                raise ValueError("No existe el producto asociado al stock.")

            stock = Stock(
                producto,
                int(fila["cantidad"]),
            )

            repo_stock.crear(stock)

        except ValueError:
            pass

    for fila in _leer_csv("cotizaciones_dolar.csv", base_path):
        try:
            tipo = repo_tipo_cotizacion.leer_por_id(int(fila["tipo_id"]))

            if tipo is None:
                raise ValueError("No existe el tipo de cotización asociado.")

            fecha = datetime.date.fromisoformat(fila["fecha"])

            cotizacion = CotizacionDolar(
                float(fila["valor"]),
                fecha=fecha,
                tipo=tipo,
            )

            repo_cotizacion.crear(cotizacion)

        except ValueError:
            pass
