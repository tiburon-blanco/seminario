"""Clases responsables de la lógica de negocio del sistema."""

import datetime

from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  Precio,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)
from price_manager.repositories.repositories import (
  RepositorioCategoria,
  RepositorioCotizacionDolar,
  RepositorioProducto,
  RepositorioProveedor,
  RepositorioStock,
)


class ServicioCategoria:
  """Aplica lógica de negocio para categorías."""

  def __init__(self, repositorio: RepositorioCategoria) -> None:
    self._repositorio = repositorio

  def crear_categoria(self, id_categoria: int, nombre: str) -> Categoria:
    """Crea una categoría validando nombre único."""
    categorias = self._repositorio.leer_todos()

    for categoria in categorias:
      if categoria.nombre.lower() == nombre.strip().lower():
        raise ValueError("Ya existe una categoría con ese nombre.")

    nueva_categoria = Categoria(id_categoria, nombre)
    return self._repositorio.crear(nueva_categoria)

  def obtener_categoria(self, id_categoria: int) -> Categoria | None:
    """Obtiene una categoría por id."""
    return self._repositorio.leer_por_id(id_categoria)

  def listar_categorias(self) -> list[Categoria]:
    """Devuelve todas las categorías."""
    return self._repositorio.leer_todos()

  def actualizar_categoria(self, id_categoria: int, nombre: str) -> Categoria:
    """Actualiza una categoría existente validando nombre único."""
    categoria_existente = self._repositorio.leer_por_id(id_categoria)

    if categoria_existente is None:
      raise ValueError("No existe una categoría con ese id.")

    categorias = self._repositorio.leer_todos()
    for categoria in categorias:
      if (
        categoria.id != id_categoria and
        categoria.nombre.lower() == nombre.strip().lower()
      ):
        raise ValueError("Ya existe otra categoría con ese nombre.")

    categoria_actualizada = Categoria(id_categoria, nombre)
    return self._repositorio.actualizar(categoria_actualizada)

  def eliminar_categoria(self, id_categoria: int) -> bool:
    """Elimina una categoría por id."""
    return self._repositorio.eliminar(id_categoria)


class ServicioProveedor:
  """Aplica lógica de negocio para proveedores."""

  def __init__(self, repositorio: RepositorioProveedor) -> None:
    self._repositorio = repositorio

  def crear_proveedor(
    self,
    id_proveedor: int,
    nombre: str,
    contacto: str
  ) -> Proveedor:
    """Crea un proveedor validando nombre único."""
    proveedores = self._repositorio.leer_todos()

    for proveedor in proveedores:
      if proveedor.nombre.lower() == nombre.strip().lower():
        raise ValueError("Ya existe un proveedor con ese nombre.")

    nuevo_proveedor = Proveedor(id_proveedor, nombre, contacto)
    return self._repositorio.crear(nuevo_proveedor)

  def obtener_proveedor(self, id_proveedor: int) -> Proveedor | None:
    """Obtiene un proveedor por id."""
    return self._repositorio.leer_por_id(id_proveedor)

  def listar_proveedores(self) -> list[Proveedor]:
    """Devuelve todos los proveedores."""
    return self._repositorio.leer_todos()

  def actualizar_proveedor(
    self,
    id_proveedor: int,
    nombre: str,
    contacto: str
  ) -> Proveedor:
    """Actualiza un proveedor existente validando nombre único."""
    proveedor_existente = self._repositorio.leer_por_id(id_proveedor)

    if proveedor_existente is None:
      raise ValueError("No existe un proveedor con ese id.")

    proveedores = self._repositorio.leer_todos()
    for proveedor in proveedores:
      if (
        proveedor.id != id_proveedor and
        proveedor.nombre.lower() == nombre.strip().lower()
      ):
        raise ValueError("Ya existe otro proveedor con ese nombre.")

    proveedor_actualizado = Proveedor(id_proveedor, nombre, contacto)
    return self._repositorio.actualizar(proveedor_actualizado)

  def eliminar_proveedor(self, id_proveedor: int) -> bool:
    """Elimina un proveedor por id."""
    return self._repositorio.eliminar(id_proveedor)


class ServicioProducto:
  """Aplica lógica de negocio para productos."""

  def __init__(self, repositorio: RepositorioProducto) -> None:
    self._repositorio = repositorio

  def crear_producto(
    self,
    id_producto: int,
    nombre: str,
    descripcion: str,
    precio: Precio,
    categoria: Categoria,
    proveedor: Proveedor
  ) -> Producto:
    """Crea un producto validando nombre único."""
    productos = self._repositorio.leer_todos()

    for producto in productos:
      if producto.nombre.lower() == nombre.strip().lower():
        raise ValueError("Ya existe un producto con ese nombre.")

    nuevo_producto = Producto(
      id_producto,
      nombre,
      descripcion,
      precio,
      categoria,
      proveedor,
    )
    return self._repositorio.crear(nuevo_producto)

  def obtener_producto(self, id_producto: int) -> Producto | None:
    """Obtiene un producto por id."""
    return self._repositorio.leer_por_id(id_producto)

  def listar_productos(self) -> list[Producto]:
    """Devuelve todos los productos."""
    return self._repositorio.leer_todos()

  def actualizar_producto(
    self,
    id_producto: int,
    nombre: str,
    descripcion: str,
    precio: Precio,
    categoria: Categoria,
    proveedor: Proveedor
  ) -> Producto:
    """Actualiza un producto existente validando nombre único."""
    producto_existente = self._repositorio.leer_por_id(id_producto)

    if producto_existente is None:
      raise ValueError("No existe un producto con ese id.")

    productos = self._repositorio.leer_todos()
    for producto in productos:
      if (
        producto.id != id_producto and
        producto.nombre.lower() == nombre.strip().lower()
      ):
        raise ValueError("Ya existe otro producto con ese nombre.")

    producto_actualizado = Producto(
      id_producto,
      nombre,
      descripcion,
      precio,
      categoria,
      proveedor,
    )
    return self._repositorio.actualizar(producto_actualizado)

  def eliminar_producto(self, id_producto: int) -> bool:
    """Elimina un producto por id."""
    return self._repositorio.eliminar(id_producto)


class ServicioStock:
  """Aplica lógica de negocio para stock."""

  def __init__(
    self,
    repositorio_stock: RepositorioStock,
    repositorio_producto: RepositorioProducto
  ) -> None:
    self._repositorio_stock = repositorio_stock
    self._repositorio_producto = repositorio_producto

  def crear_stock(self, id_producto: int, cantidad: int) -> Stock:
    """Crea un stock validando que el producto exista."""
    producto = self._repositorio_producto.leer_por_id(id_producto)

    if producto is None:
      raise ValueError("No existe un producto con ese id.")

    nuevo_stock = Stock(producto, cantidad)
    return self._repositorio_stock.crear(nuevo_stock)

  def obtener_stock(self, id_producto: int) -> Stock | None:
    """Obtiene el stock de un producto."""
    return self._repositorio_stock.leer_por_producto(id_producto)

  def listar_stocks(self) -> list[Stock]:
    """Devuelve todos los stocks."""
    return self._repositorio_stock.leer_todos()

  def actualizar_stock(self, id_producto: int, cantidad: int) -> Stock:
    """Actualiza el stock de un producto existente."""
    producto = self._repositorio_producto.leer_por_id(id_producto)

    if producto is None:
      raise ValueError("No existe un producto con ese id.")

    stock_actualizado = Stock(producto, cantidad)
    return self._repositorio_stock.actualizar(stock_actualizado)

  def eliminar_stock(self, id_producto: int) -> bool:
    """Elimina el stock de un producto."""
    return self._repositorio_stock.eliminar(id_producto)


class ServicioCotizacionDolar:
  """Aplica lógica de negocio para cotizaciones de dólar."""

  def __init__(self, repositorio: RepositorioCotizacionDolar) -> None:
    self._repositorio = repositorio

  def crear_cotizacion(
    self,
    valor: float,
    tipo: TipoCotizacion,
    fecha: datetime.date | None = None
  ) -> CotizacionDolar:
    """Crea una cotización de dólar."""
    nueva_cotizacion = CotizacionDolar(valor, fecha=fecha, tipo=tipo)
    return self._repositorio.crear(nueva_cotizacion)

  def obtener_cotizacion(
    self,
    tipo_id: int,
    fecha: datetime.date
  ) -> CotizacionDolar | None:
    """Obtiene una cotización por tipo y fecha."""
    return self._repositorio.leer_por_tipo_y_fecha(tipo_id, fecha)

  def listar_historico(self, tipo_id: int) -> list[CotizacionDolar]:
    """Devuelve el histórico de cotizaciones de un tipo."""
    return self._repositorio.leer_historico_por_tipo(tipo_id)

  def listar_todas(self) -> list[CotizacionDolar]:
    """Devuelve todas las cotizaciones."""
    return self._repositorio.leer_todos()

  def actualizar_cotizacion(
    self,
    valor: float,
    tipo: TipoCotizacion,
    fecha: datetime.date
  ) -> CotizacionDolar:
    """Actualiza una cotización existente."""
    cotizacion_actualizada = CotizacionDolar(
      valor,
      fecha=fecha,
      tipo=tipo,
    )
    return self._repositorio.actualizar(cotizacion_actualizada)

  def eliminar_cotizacion(
    self,
    tipo_id: int,
    fecha: datetime.date
  ) -> bool:
    """Elimina una cotización."""
    return self._repositorio.eliminar(tipo_id, fecha)
