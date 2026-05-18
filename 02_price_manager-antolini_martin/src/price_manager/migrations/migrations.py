"""Migracion de datos CSV a SQL y base relacional."""

import csv
import datetime
import os
from pathlib import Path

from price_manager.database.connection import ConexionDB
from price_manager.models.models import (
  CategoriaModel,
  CotizacionDolarModel,
  MonedaModel,
  ProductoModel,
  ProveedorModel,
  StockModel,
  TipoCotizacionModel,
)


def _leer_csv(ruta: str) -> list[dict[str, str]]:
  with open(ruta, mode="r", encoding="utf-8") as archivo:
    return list(csv.DictReader(archivo))


def _valor_sql(valor: str) -> str:
  valor_limpio = str(valor).replace("'", "''")
  return f"'{valor_limpio}'"


def _guardar_sql(
  carpeta_sqls: str,
  tabla: str,
  filas: list[dict[str, str]],
) -> None:
  Path(carpeta_sqls).mkdir(parents=True, exist_ok=True)
  ruta_sql = os.path.join(carpeta_sqls, f"{tabla}.sql")
  if not filas:
    return

  columnas = list(filas[0].keys())
  with open(ruta_sql, mode="w", encoding="utf-8") as archivo:
    for fila in filas:
      valores = ", ".join(_valor_sql(fila[columna]) for columna in columnas)
      columnas_sql = ", ".join(columnas)
      archivo.write(
        f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({valores});\n"
      )


def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> None:
  """Migra los CSV del Sprint 1 a SQL y a la base de datos."""
  conexion = ConexionDB()
  conexion.crear_tablas()

  categorias = _leer_csv(os.path.join(carpeta_csvs, "categorias.csv"))
  proveedores = _leer_csv(os.path.join(carpeta_csvs, "proveedores.csv"))
  monedas = _leer_csv(os.path.join(carpeta_csvs, "monedas.csv"))
  tipos = _leer_csv(os.path.join(carpeta_csvs, "tipos_cotizacion.csv"))
  productos = _leer_csv(os.path.join(carpeta_csvs, "productos.csv"))
  stocks = _leer_csv(os.path.join(carpeta_csvs, "stock.csv"))
  cotizaciones = _leer_csv(
    os.path.join(carpeta_csvs, "cotizaciones_dolar.csv")
  )

  _guardar_sql(carpeta_sqls, "categorias", categorias)
  _guardar_sql(carpeta_sqls, "proveedores", proveedores)
  _guardar_sql(carpeta_sqls, "monedas", monedas)
  _guardar_sql(carpeta_sqls, "tipos_cotizacion", tipos)
  _guardar_sql(carpeta_sqls, "productos", productos)
  _guardar_sql(carpeta_sqls, "stock", stocks)
  _guardar_sql(carpeta_sqls, "cotizaciones_dolar", cotizaciones)

  with conexion.obtener_sesion() as session:
    for fila in monedas:
      session.merge(MonedaModel(id=int(fila["id"]), nombre=fila["nombre"]))
    for fila in tipos:
      session.merge(
        TipoCotizacionModel(id=int(fila["id"]), nombre=fila["nombre"])
      )
    for fila in categorias:
      session.merge(
        CategoriaModel(id=int(fila["id"]), nombre=fila["nombre"])
      )
    for fila in proveedores:
      session.merge(
        ProveedorModel(
          id=int(fila["id"]),
          nombre=fila["nombre"],
          contacto=fila["contacto"],
        )
      )
    for fila in productos:
      session.merge(
        ProductoModel(
          id=int(fila["id"]),
          nombre=fila["nombre"],
          descripcion=fila["descripcion"],
          precio_valor=float(fila["precio_valor"]),
          moneda_id=int(fila["moneda_id"]),
          precio_fecha=datetime.date.fromisoformat(fila["precio_fecha"]),
          categoria_id=int(fila["categoria_id"]),
          proveedor_id=int(fila["proveedor_id"]),
        )
      )
    for fila in stocks:
      session.merge(
        StockModel(
          producto_id=int(fila["producto_id"]),
          cantidad=int(fila["cantidad"]),
        )
      )
    for fila in cotizaciones:
      session.merge(
        CotizacionDolarModel(
          tipo_id=int(fila["tipo_id"]),
          fecha=datetime.date.fromisoformat(fila["fecha"]),
          valor=float(fila["valor"]),
        )
      )
