"""Interfaz de usuario por consola para el sistema Price Manager."""

import datetime
import os

from price_manager.database.connection import ConexionDB
from price_manager.entities.entities import Precio
from price_manager.migrations.migrations import migrar_datos
from price_manager.repositories.repositories import (
  RepositorioCategoria,
  RepositorioCotizacionDolar,
  RepositorioMoneda,
  RepositorioProducto,
  RepositorioProveedor,
  RepositorioStock,
  RepositorioTipoCotizacion,
)
from price_manager.services.services import (
  ServicioCategoria,
  ServicioCotizacionDolar,
  ServicioProducto,
  ServicioProveedor,
  ServicioStock,
)


class ConsolaPriceManager:
  """Interfaz de consola del sistema."""

  def __init__(self) -> None:
    self.conexion = ConexionDB()
    self.conexion.crear_tablas()

    self.repo_categoria = RepositorioCategoria(self.conexion)
    self.repo_proveedor = RepositorioProveedor(self.conexion)
    self.repo_moneda = RepositorioMoneda(self.conexion)
    self.repo_tipo_cotizacion = RepositorioTipoCotizacion(self.conexion)
    self.repo_producto = RepositorioProducto(self.conexion)
    self.repo_stock = RepositorioStock(self.conexion)
    self.repo_cotizacion = RepositorioCotizacionDolar(self.conexion)

    self._migrar_datos_iniciales()

    self.servicio_categoria = ServicioCategoria(self.repo_categoria)
    self.servicio_proveedor = ServicioProveedor(self.repo_proveedor)
    self.servicio_producto = ServicioProducto(self.repo_producto)
    self.servicio_stock = ServicioStock(
      self.repo_stock,
      self.repo_producto,
    )
    self.servicio_cotizacion = ServicioCotizacionDolar(
      self.repo_cotizacion,
      self.repo_tipo_cotizacion,
    )

  def _migrar_datos_iniciales(self) -> None:
    """Carga los CSV iniciales si la base se encuentra vacia."""
    if self.repo_categoria.leer_todos():
      return

    base = os.path.dirname(os.path.dirname(__file__))
    carpeta_csvs = os.path.join(base, "migrations", "csv")
    carpeta_sqls = os.path.join(base, "migrations", "sql")
    migrar_datos(carpeta_csvs, carpeta_sqls)

  def mostrar_menu_principal(self) -> None:
    """Muestra el menú principal."""
    print("\n=== PRICE MANAGER ===")
    print("1. Gestionar categorías")
    print("2. Gestionar proveedores")
    print("3. Gestionar productos")
    print("4. Gestionar stock")
    print("5. Gestionar cotizaciones")
    print("6. Obtener cotizaciones por API")
    print("7. Ver lista de precios bimonetaria")
    print("8. Exportar precios a CSV")
    print("0. Salir")

  def ejecutar(self) -> None:
    """Ejecuta la interfaz principal."""
    while True:
      self.mostrar_menu_principal()
      opcion = input("Seleccione una opción: ").strip()

      if opcion == "1":
        self.menu_categorias()
      elif opcion == "2":
        self.menu_proveedores()
      elif opcion == "3":
        self.menu_productos()
      elif opcion == "4":
        self.menu_stock()
      elif opcion == "5":
        self.menu_cotizaciones()
      elif opcion == "6":
        self.obtener_cotizaciones_api()
      elif opcion == "7":
        self.ver_precios_bimonetarios()
      elif opcion == "8":
        self.exportar_precios_csv()
      elif opcion == "0":
        print("Saliendo del sistema...")
        break
      else:
        print("Opción inválida.")

  def menu_categorias(self) -> None:
    """Menú CRUD de categorías."""
    while True:
      print("\n--- CATEGORÍAS ---")
      print("1. Crear")
      print("2. Listar")
      print("3. Actualizar")
      print("4. Eliminar")
      print("0. Volver")

      opcion = input("Seleccione una opción: ").strip()

      try:
        if opcion == "1":
          id_categoria = int(input("ID: "))
          nombre = input("Nombre: ")
          categoria = self.servicio_categoria.crear_categoria(
            id_categoria,
            nombre,
          )
          print("Categoría creada:", categoria)

        elif opcion == "2":
          categorias = self.servicio_categoria.listar_categorias()
          if not categorias:
            print("No hay categorías cargadas.")
          else:
            for categoria in categorias:
              print(categoria)

        elif opcion == "3":
          id_categoria = int(input("ID a actualizar: "))
          nombre = input("Nuevo nombre: ")
          categoria = self.servicio_categoria.actualizar_categoria(
            id_categoria,
            nombre,
          )
          print("Categoría actualizada:", categoria)

        elif opcion == "4":
          id_categoria = int(input("ID a eliminar: "))
          eliminado = self.servicio_categoria.eliminar_categoria(
            id_categoria,
          )
          print("Resultado:", eliminado)

        elif opcion == "0":
          break

        else:
          print("Opción inválida.")

      except ValueError as error:
        print("Error:", error)


def iniciar_menu() -> None:
  """Inicia el menu interactivo de Price Manager."""
  consola = ConsolaPriceManager()
  consola.ejecutar()

  def obtener_cotizaciones_api(self) -> None:
    """Obtiene cotizaciones desde la API configurada en .env."""
    try:
      cotizaciones = self.servicio_cotizacion.obtener_cotizaciones()
      print(f"Cotizaciones registradas: {len(cotizaciones)}")
      for cotizacion in cotizaciones:
        print(cotizacion)
    except Exception as error:
      print("Error al consultar la API:", error)

  def ver_precios_bimonetarios(self) -> None:
    """Muestra precios en ARS y en otra moneda seleccionada."""
    try:
      moneda = input("Moneda destino (USD): ").strip() or "USD"
      tipo = input("Tipo de dólar (Blue): ").strip() or "Blue"
      cotizacion = self.servicio_cotizacion.obtener_ultima_cotizacion(tipo)

      if cotizacion is None:
        raise ValueError("No hay cotización disponible para ese tipo.")

      precios = self.servicio_producto.listar_precios_bimonetarios(
        moneda,
        cotizacion.valor,
      )
      print(f"\nCotización usada: {cotizacion.valor:.2f} ({tipo})")
      for precio in precios:
        print(precio)
    except ValueError as error:
      print("Error:", error)

  def exportar_precios_csv(self) -> None:
    """Exporta precios en ARS y por tipos de cotización disponibles."""
    try:
      cotizaciones = self.servicio_cotizacion.listar_todas()
      ultimas = {}
      for cotizacion in cotizaciones:
        nombre = cotizacion.tipo.nombre.upper()
        actual = ultimas.get(nombre)
        if actual is None or cotizacion.fecha > actual.fecha:
          ultimas[nombre] = cotizacion

      if not ultimas:
        raise ValueError("No hay cotizaciones cargadas para exportar.")

      base = os.path.dirname(os.path.dirname(__file__))
      ruta = os.path.join(base, "migrations", "csv", "precios_exportados.csv")
      valores = {
        nombre: cotizacion.valor for nombre, cotizacion in ultimas.items()
      }
      self.servicio_producto.exportar_precios_csv(ruta, valores)
      print("Archivo exportado:", ruta)
    except ValueError as error:
      print("Error:", error)

  def menu_proveedores(self) -> None:
    """Menú CRUD de proveedores."""
    while True:
      print("\n--- PROVEEDORES ---")
      print("1. Crear")
      print("2. Listar")
      print("3. Actualizar")
      print("4. Eliminar")
      print("5. Obtener cotizaciones por API")
      print("0. Volver")

      opcion = input("Seleccione una opción: ").strip()

      try:
        if opcion == "1":
          id_proveedor = int(input("ID: "))
          nombre = input("Nombre: ")
          contacto = input("Contacto: ")
          proveedor = self.servicio_proveedor.crear_proveedor(
            id_proveedor,
            nombre,
            contacto,
          )
          print("Proveedor creado:", proveedor)

        elif opcion == "2":
          proveedores = self.servicio_proveedor.listar_proveedores()
          if not proveedores:
            print("No hay proveedores cargados.")
          else:
            for proveedor in proveedores:
              print(proveedor)

        elif opcion == "3":
          id_proveedor = int(input("ID a actualizar: "))
          nombre = input("Nuevo nombre: ")
          contacto = input("Nuevo contacto: ")
          proveedor = self.servicio_proveedor.actualizar_proveedor(
            id_proveedor,
            nombre,
            contacto,
          )
          print("Proveedor actualizado:", proveedor)

        elif opcion == "4":
          id_proveedor = int(input("ID a eliminar: "))
          eliminado = self.servicio_proveedor.eliminar_proveedor(
            id_proveedor,
          )
          print("Resultado:", eliminado)

        elif opcion == "0":
          break

        else:
          print("Opción inválida.")

      except ValueError as error:
        print("Error:", error)

  def menu_productos(self) -> None:
    """Menú CRUD de productos."""
    while True:
      print("\n--- PRODUCTOS ---")
      print("1. Crear")
      print("2. Listar")
      print("3. Actualizar")
      print("4. Eliminar")
      print("5. Obtener cotizaciones por API")
      print("0. Volver")

      opcion = input("Seleccione una opción: ").strip()

      try:
        if opcion == "1":
          id_producto = int(input("ID: "))
          nombre = input("Nombre: ")
          descripcion = input("Descripción: ")
          precio_valor = float(input("Precio: "))
          categoria_id = int(input("ID categoría: "))
          proveedor_id = int(input("ID proveedor: "))

          categoria = self.servicio_categoria.obtener_categoria(
            categoria_id,
          )
          proveedor = self.servicio_proveedor.obtener_proveedor(
            proveedor_id,
          )
          moneda = self.repo_moneda.leer_por_id(1)

          if categoria is None:
            raise ValueError("La categoría no existe.")
          if proveedor is None:
            raise ValueError("El proveedor no existe.")
          if moneda is None:
            raise ValueError("No existe la moneda base.")

          precio = Precio(precio_valor, moneda)

          producto = self.servicio_producto.crear_producto(
            id_producto,
            nombre,
            descripcion,
            precio,
            categoria,
            proveedor,
          )
          print("Producto creado:", producto)

        elif opcion == "2":
          productos = self.servicio_producto.listar_productos()
          if not productos:
            print("No hay productos cargados.")
          else:
            for producto in productos:
              print(producto)

        elif opcion == "3":
          id_producto = int(input("ID a actualizar: "))
          nombre = input("Nuevo nombre: ")
          descripcion = input("Nueva descripción: ")
          precio_valor = float(input("Nuevo precio: "))
          categoria_id = int(input("ID categoría: "))
          proveedor_id = int(input("ID proveedor: "))

          categoria = self.servicio_categoria.obtener_categoria(
            categoria_id,
          )
          proveedor = self.servicio_proveedor.obtener_proveedor(
            proveedor_id,
          )
          moneda = self.repo_moneda.leer_por_id(1)

          if categoria is None:
            raise ValueError("La categoría no existe.")
          if proveedor is None:
            raise ValueError("El proveedor no existe.")
          if moneda is None:
            raise ValueError("No existe la moneda base.")

          precio = Precio(precio_valor, moneda)

          producto = self.servicio_producto.actualizar_producto(
            id_producto,
            nombre,
            descripcion,
            precio,
            categoria,
            proveedor,
          )
          print("Producto actualizado:", producto)

        elif opcion == "4":
          id_producto = int(input("ID a eliminar: "))
          eliminado = self.servicio_producto.eliminar_producto(
            id_producto,
          )
          print("Resultado:", eliminado)

        elif opcion == "0":
          break

        else:
          print("Opción inválida.")

      except ValueError as error:
        print("Error:", error)

  def menu_stock(self) -> None:
    """Menú CRUD de stock."""
    while True:
      print("\n--- STOCK ---")
      print("1. Crear")
      print("2. Listar")
      print("3. Actualizar")
      print("4. Eliminar")
      print("0. Volver")

      opcion = input("Seleccione una opción: ").strip()

      try:
        if opcion == "1":
          id_producto = int(input("ID producto: "))
          cantidad = int(input("Cantidad: "))
          stock = self.servicio_stock.crear_stock(
            id_producto,
            cantidad,
          )
          print("Stock creado:", stock)

        elif opcion == "2":
          stocks = self.servicio_stock.listar_stocks()
          if not stocks:
            print("No hay stock cargado.")
          else:
            for stock in stocks:
              print(stock)

        elif opcion == "3":
          id_producto = int(input("ID producto: "))
          cantidad = int(input("Nueva cantidad: "))
          stock = self.servicio_stock.actualizar_stock(
            id_producto,
            cantidad,
          )
          print("Stock actualizado:", stock)

        elif opcion == "4":
          id_producto = int(input("ID producto: "))
          eliminado = self.servicio_stock.eliminar_stock(
            id_producto,
          )
          print("Resultado:", eliminado)

        elif opcion == "0":
          break

        else:
          print("Opción inválida.")

      except ValueError as error:
        print("Error:", error)

  def menu_cotizaciones(self) -> None:
    """Menú CRUD de cotizaciones de dólar."""
    while True:
      print("\n--- COTIZACIONES ---")
      print("1. Crear")
      print("2. Listar")
      print("3. Actualizar")
      print("4. Eliminar")
      print("0. Volver")

      opcion = input("Seleccione una opción: ").strip()

      try:
        if opcion == "1":
          valor = float(input("Valor: "))
          tipo_id = int(input("ID tipo de cotización: "))
          fecha = datetime.date.fromisoformat(
            input("Fecha (YYYY-MM-DD): ")
          )

          tipo = self.repo_tipo_cotizacion.leer_por_id(tipo_id)
          if tipo is None:
            raise ValueError("No existe el tipo de cotización.")

          cotizacion = self.servicio_cotizacion.crear_cotizacion(
            valor,
            tipo,
            fecha,
          )
          print("Cotización creada:", cotizacion)

        elif opcion == "2":
          cotizaciones = self.servicio_cotizacion.listar_todas()
          if not cotizaciones:
            print("No hay cotizaciones cargadas.")
          else:
            for cotizacion in cotizaciones:
              print(cotizacion)

        elif opcion == "3":
          valor = float(input("Nuevo valor: "))
          tipo_id = int(input("ID tipo de cotización: "))
          fecha = datetime.date.fromisoformat(
            input("Fecha (YYYY-MM-DD): ")
          )

          tipo = self.repo_tipo_cotizacion.leer_por_id(tipo_id)
          if tipo is None:
            raise ValueError("No existe el tipo de cotización.")

          cotizacion = self.servicio_cotizacion.actualizar_cotizacion(
            valor,
            tipo,
            fecha,
          )
          print("Cotización actualizada:", cotizacion)

        elif opcion == "4":
          tipo_id = int(input("ID tipo de cotización: "))
          fecha = datetime.date.fromisoformat(
            input("Fecha (YYYY-MM-DD): ")
          )
          eliminado = self.servicio_cotizacion.eliminar_cotizacion(
            tipo_id,
            fecha,
          )
          print("Resultado:", eliminado)

        elif opcion == "5":
          self.obtener_cotizaciones_api()

        elif opcion == "0":
          break

        else:
          print("Opción inválida.")

      except ValueError as error:
        print("Error:", error)
