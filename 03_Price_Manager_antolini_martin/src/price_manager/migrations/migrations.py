"""Migracion de datos CSV a SQL y base relacional."""

import csv
import datetime
import os
from pathlib import Path

from sqlalchemy import text

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
  """Lee un archivo CSV y devuelve una lista de diccionarios."""
  with open(ruta, mode="r", encoding="utf-8") as archivo:
    return list(csv.DictReader(archivo))


def _valor_sql(valor: str) -> str:
  """Convierte un valor en un literal SQL simple."""
  valor_limpio = str(valor).replace("'", "''")
  return f"'{valor_limpio}'"


def _guardar_sql(
  carpeta_sqls: str,
  tabla: str,
  filas: list[dict[str, str]],
) -> None:
  """Guarda sentencias INSERT en un archivo SQL."""
  Path(carpeta_sqls).mkdir(parents=True, exist_ok=True)

  if not filas:
    return

  ruta_sql = os.path.join(carpeta_sqls, f"{tabla}.sql")
  columnas = list(filas[0].keys())

  with open(ruta_sql, mode="w", encoding="utf-8") as archivo:
    for fila in filas:
      valores = ", ".join(_valor_sql(fila[columna]) for columna in columnas)
      columnas_sql = ", ".join(columnas)
      archivo.write(
        f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({valores});\n"
      )


def _orden_archivos_sql() -> list[str]:
  """Define el orden correcto de carga de archivos SQL."""
  return [
    "monedas.sql",
    "tipos_cotizacion.sql",
    "categorias.sql",
    "proveedores.sql",
    "productos.sql",
    "stock.sql",
    "cotizaciones_dolar.sql",
  ]


def cargar_datos_desde_sql(
  ruta_sql: str,
  conexion: ConexionDB | None = None,
) -> int:
  """Carga datos en la base ejecutando un archivo SQL.

  Args:
    ruta_sql: Ruta del archivo .sql a ejecutar.
    conexion: Conexión opcional. Si no se informa, se crea una nueva.

  Returns:
    Cantidad de sentencias ejecutadas.
  """
  archivo_sql = Path(ruta_sql)

  if not archivo_sql.exists():
    raise FileNotFoundError(f"No existe el archivo SQL: {archivo_sql}")

  if archivo_sql.suffix.lower() != ".sql":
    raise ValueError("El archivo indicado debe tener extensión .sql")

  conexion_db = conexion or ConexionDB()
  conexion_db.crear_tablas()

  contenido_sql = archivo_sql.read_text(encoding="utf-8")

  sentencias = [
    sentencia.strip()
    for sentencia in contenido_sql.split(";")
    if sentencia.strip()
  ]

  sentencias_ejecutadas = 0

  with conexion_db.engine.begin() as connection:
    for sentencia in sentencias:
      sentencia = sentencia.replace(
        "INSERT INTO",
        "INSERT OR IGNORE INTO",
      )
      connection.execute(text(sentencia))
      sentencias_ejecutadas += 1

  return sentencias_ejecutadas


def cargar_desde_sql(
  carpeta_sqls: str,
  conexion: ConexionDB | None = None,
) -> int:
  """Carga datos iniciales desde los archivos SQL de una carpeta.

  Args:
    carpeta_sqls: Carpeta donde se encuentran los archivos .sql.
    conexion: Conexión opcional. Si no se informa, se crea una nueva.

  Returns:
    Cantidad total de sentencias ejecutadas.
  """
  conexion_db = conexion or ConexionDB()
  conexion_db.crear_tablas()

  sentencias_ejecutadas = 0

  for nombre_archivo in _orden_archivos_sql():
    ruta_sql = os.path.join(carpeta_sqls, nombre_archivo)

    if not os.path.exists(ruta_sql):
      continue

    sentencias_ejecutadas += cargar_datos_desde_sql(
      ruta_sql=ruta_sql,
      conexion=conexion_db,
    )

  return sentencias_ejecutadas


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
      session.merge(
        MonedaModel(
          id=int(fila["id"]),
          nombre=fila["nombre"],
        )
      )

    for fila in tipos:
      session.merge(
        TipoCotizacionModel(
          id=int(fila["id"]),
          nombre=fila["nombre"],
        )
      )

    for fila in categorias:
      session.merge(
        CategoriaModel(
          id=int(fila["id"]),
          nombre=fila["nombre"],
        )
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