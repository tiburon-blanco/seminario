"""Repositorios SQLAlchemy para la persistencia del sistema."""

import abc
import datetime
from typing import Generic, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from price_manager.database.connection import ConexionDB, conexion_db
from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  EntidadBase,
  Moneda,
  Precio,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)
from price_manager.models.models import (
  CategoriaModel,
  CotizacionDolarModel,
  MonedaModel,
  ProductoModel,
  ProveedorModel,
  StockModel,
  TipoCotizacionModel,
)

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz generica para repositorios CRUD."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    """Crea una entidad."""

  @abc.abstractmethod
  def leer_por_id(self, id_entidad: int) -> Optional[T]:
    """Lee una entidad por id."""

  @abc.abstractmethod
  def leer_todos(self) -> list[T]:
    """Lee todas las entidades."""

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad."""

  @abc.abstractmethod
  def eliminar(self, id_entidad: int) -> bool:
    """Elimina una entidad por id."""


class IRepositorioStock(abc.ABC):
  """Interfaz para el repositorio de stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    """Crea un registro de stock."""

  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    """Lee stock por producto."""

  @abc.abstractmethod
  def leer_todos(self) -> list[Stock]:
    """Lee todos los registros de stock."""

  @abc.abstractmethod
  def actualizar(self, stock: Stock) -> Stock:
    """Actualiza stock."""

  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool:
    """Elimina stock por producto."""


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz para el repositorio de cotizaciones."""

  @abc.abstractmethod
  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Crea una cotizacion."""

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(
    self,
    tipo_id: int,
    fecha: datetime.date,
  ) -> Optional[CotizacionDolar]:
    """Lee una cotizacion por tipo y fecha."""

  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> list[CotizacionDolar]:
    """Lee el historico de un tipo."""

  @abc.abstractmethod
  def leer_todos(self) -> list[CotizacionDolar]:
    """Lee todas las cotizaciones."""

  @abc.abstractmethod
  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Actualiza una cotizacion."""

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotizacion."""


def _a_categoria(modelo: CategoriaModel) -> Categoria:
  return Categoria(modelo.id, modelo.nombre)


def _a_proveedor(modelo: ProveedorModel) -> Proveedor:
  return Proveedor(modelo.id, modelo.nombre, modelo.contacto)


def _a_moneda(modelo: MonedaModel) -> Moneda:
  return Moneda(modelo.id, modelo.nombre)


def _a_tipo(modelo: TipoCotizacionModel) -> TipoCotizacion:
  return TipoCotizacion(modelo.id, modelo.nombre)


def _a_producto(modelo: ProductoModel) -> Producto:
  moneda = _a_moneda(modelo.moneda)
  precio = Precio(modelo.precio_valor, moneda, modelo.precio_fecha)
  return Producto(
    modelo.id,
    modelo.nombre,
    modelo.descripcion,
    precio,
    _a_categoria(modelo.categoria),
    _a_proveedor(modelo.proveedor),
  )


def _a_stock(modelo: StockModel) -> Stock:
  return Stock(_a_producto(modelo.producto), modelo.cantidad)


def _a_cotizacion(modelo: CotizacionDolarModel) -> CotizacionDolar:
  return CotizacionDolar(modelo.valor, modelo.fecha, _a_tipo(modelo.tipo))


class RepositorioBase(IRepositorio[T]):
  """Repositorio base para tablas con clave primaria id."""

  def __init__(self, conexion: ConexionDB | None = None) -> None:
    self._conexion = conexion or conexion_db

  def crear(self, entidad: T) -> T:
    """Crea una entidad si no existe el id."""
    with self._conexion.obtener_sesion() as session:
      if session.get(self._modelo, entidad.id) is not None:
        raise ValueError(f"Ya existe una entidad con id {entidad.id}.")
      modelo = self._desde_entidad(entidad)
      session.add(modelo)
      session.flush()
      return self._a_entidad(modelo)

  def leer_por_id(self, id_entidad: int) -> Optional[T]:
    """Lee una entidad por id."""
    with self._conexion.obtener_sesion() as session:
      modelo = session.get(self._modelo, id_entidad)
      if modelo is None:
        return None
      return self._a_entidad(modelo)

  def leer_todos(self) -> list[T]:
    """Lee todas las entidades."""
    with self._conexion.obtener_sesion() as session:
      modelos = session.scalars(select(self._modelo)).all()
      return [self._a_entidad(modelo) for modelo in modelos]

  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente."""
    with self._conexion.obtener_sesion() as session:
      if session.get(self._modelo, entidad.id) is None:
        raise ValueError(f"No existe una entidad con id {entidad.id}.")
      modelo = session.merge(self._desde_entidad(entidad))
      session.flush()
      return self._a_entidad(modelo)

  def eliminar(self, id_entidad: int) -> bool:
    """Elimina una entidad por id."""
    with self._conexion.obtener_sesion() as session:
      modelo = session.get(self._modelo, id_entidad)
      if modelo is None:
        return False
      session.delete(modelo)
      return True


class RepositorioCategoria(RepositorioBase[Categoria]):
  """Repositorio de categorias."""

  _modelo = CategoriaModel
  _a_entidad = staticmethod(_a_categoria)

  def _desde_entidad(self, entidad: Categoria) -> CategoriaModel:
    return CategoriaModel(id=entidad.id, nombre=entidad.nombre)


class RepositorioProveedor(RepositorioBase[Proveedor]):
  """Repositorio de proveedores."""

  _modelo = ProveedorModel
  _a_entidad = staticmethod(_a_proveedor)

  def _desde_entidad(self, entidad: Proveedor) -> ProveedorModel:
    return ProveedorModel(
      id=entidad.id,
      nombre=entidad.nombre,
      contacto=entidad.contacto,
    )


class RepositorioMoneda(RepositorioBase[Moneda]):
  """Repositorio de monedas."""

  _modelo = MonedaModel
  _a_entidad = staticmethod(_a_moneda)

  def _desde_entidad(self, entidad: Moneda) -> MonedaModel:
    return MonedaModel(id=entidad.id, nombre=entidad.nombre)


class RepositorioTipoCotizacion(RepositorioBase[TipoCotizacion]):
  """Repositorio de tipos de cotizacion."""

  _modelo = TipoCotizacionModel
  _a_entidad = staticmethod(_a_tipo)

  def _desde_entidad(self, entidad: TipoCotizacion) -> TipoCotizacionModel:
    return TipoCotizacionModel(id=entidad.id, nombre=entidad.nombre)


class RepositorioProducto(RepositorioBase[Producto]):
  """Repositorio de productos."""

  _modelo = ProductoModel

  def _desde_entidad(self, entidad: Producto) -> ProductoModel:
    return ProductoModel(
      id=entidad.id,
      nombre=entidad.nombre,
      descripcion=entidad.descripcion,
      precio_valor=entidad.precio.valor,
      moneda_id=entidad.precio.moneda.id,
      precio_fecha=entidad.precio.fecha,
      categoria_id=entidad.categoria.id,
      proveedor_id=entidad.proveedor.id,
    )

  def leer_por_id(self, id_entidad: int) -> Optional[Producto]:
    """Lee un producto por id con sus relaciones."""
    with self._conexion.obtener_sesion() as session:
      sentencia = (
        select(ProductoModel)
        .options(
          selectinload(ProductoModel.moneda),
          selectinload(ProductoModel.categoria),
          selectinload(ProductoModel.proveedor),
        )
        .where(ProductoModel.id == id_entidad)
      )
      modelo = session.scalars(sentencia).first()
      return None if modelo is None else _a_producto(modelo)

  def leer_todos(self) -> list[Producto]:
    """Lee todos los productos con sus relaciones."""
    with self._conexion.obtener_sesion() as session:
      sentencia = select(ProductoModel).options(
        selectinload(ProductoModel.moneda),
        selectinload(ProductoModel.categoria),
        selectinload(ProductoModel.proveedor),
      )
      return [_a_producto(modelo) for modelo in session.scalars(sentencia)]

  def crear(self, entidad: Producto) -> Producto:
    """Crea un producto."""
    with self._conexion.obtener_sesion() as session:
      if session.get(ProductoModel, entidad.id) is not None:
        raise ValueError(f"Ya existe una entidad con id {entidad.id}.")
      session.add(self._desde_entidad(entidad))
    producto = self.leer_por_id(entidad.id)
    if producto is None:
      raise ValueError("No se pudo recuperar el producto creado.")
    return producto

  def actualizar(self, entidad: Producto) -> Producto:
    """Actualiza un producto."""
    with self._conexion.obtener_sesion() as session:
      if session.get(ProductoModel, entidad.id) is None:
        raise ValueError(f"No existe una entidad con id {entidad.id}.")
      session.merge(self._desde_entidad(entidad))
      session.flush()
    producto = self.leer_por_id(entidad.id)
    if producto is None:
      raise ValueError("No se pudo recuperar el producto actualizado.")
    return producto


class RepositorioStock(IRepositorioStock):
  """Repositorio de stock."""

  def __init__(self, conexion: ConexionDB | None = None) -> None:
    self._conexion = conexion or conexion_db

  def crear(self, stock: Stock) -> Stock:
    """Crea un registro de stock."""
    with self._conexion.obtener_sesion() as session:
      if session.get(StockModel, stock.producto.id) is not None:
        raise ValueError("Ya existe stock para ese producto.")
      modelo = StockModel(
        producto_id=stock.producto.id,
        cantidad=stock.cantidad,
      )
      session.add(modelo)
    stock_creado = self.leer_por_producto(stock.producto.id)
    if stock_creado is None:
      raise ValueError("No se pudo recuperar el stock creado.")
    return stock_creado

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    """Lee stock por id de producto."""
    with self._conexion.obtener_sesion() as session:
      sentencia = (
        select(StockModel)
        .options(
          selectinload(StockModel.producto).selectinload(ProductoModel.moneda),
          selectinload(StockModel.producto).selectinload(
            ProductoModel.categoria,
          ),
          selectinload(StockModel.producto).selectinload(
            ProductoModel.proveedor,
          ),
        )
        .where(StockModel.producto_id == producto_id)
      )
      modelo = session.scalars(sentencia).first()
      return None if modelo is None else _a_stock(modelo)

  def leer_todos(self) -> list[Stock]:
    """Lee todos los registros de stock."""
    with self._conexion.obtener_sesion() as session:
      sentencia = select(StockModel).options(
        selectinload(StockModel.producto).selectinload(ProductoModel.moneda),
        selectinload(StockModel.producto).selectinload(ProductoModel.categoria),
        selectinload(StockModel.producto).selectinload(ProductoModel.proveedor),
      )
      return [_a_stock(modelo) for modelo in session.scalars(sentencia)]

  def actualizar(self, stock: Stock) -> Stock:
    """Actualiza stock."""
    with self._conexion.obtener_sesion() as session:
      if session.get(StockModel, stock.producto.id) is None:
        raise ValueError("No existe stock para ese producto.")
      session.merge(
        StockModel(producto_id=stock.producto.id, cantidad=stock.cantidad)
      )
    stock_actualizado = self.leer_por_producto(stock.producto.id)
    if stock_actualizado is None:
      raise ValueError("No se pudo recuperar el stock actualizado.")
    return stock_actualizado

  def eliminar(self, producto_id: int) -> bool:
    """Elimina stock por id de producto."""
    with self._conexion.obtener_sesion() as session:
      modelo = session.get(StockModel, producto_id)
      if modelo is None:
        return False
      session.delete(modelo)
      return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  """Repositorio de cotizaciones de dolar."""

  def __init__(self, conexion: ConexionDB | None = None) -> None:
    self._conexion = conexion or conexion_db

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Crea una cotizacion."""
    clave = (cotizacion.tipo.id, cotizacion.fecha)
    with self._conexion.obtener_sesion() as session:
      if session.get(CotizacionDolarModel, clave) is not None:
        raise ValueError("Ya existe una cotizacion para ese tipo y fecha.")
      modelo = CotizacionDolarModel(
        tipo_id=cotizacion.tipo.id,
        fecha=cotizacion.fecha,
        valor=cotizacion.valor,
      )
      session.add(modelo)
    cotizacion_creada = self.leer_por_tipo_y_fecha(*clave)
    if cotizacion_creada is None:
      raise ValueError("No se pudo recuperar la cotizacion creada.")
    return cotizacion_creada

  def leer_por_tipo_y_fecha(
    self,
    tipo_id: int,
    fecha: datetime.date,
  ) -> Optional[CotizacionDolar]:
    """Lee una cotizacion por tipo y fecha."""
    with self._conexion.obtener_sesion() as session:
      sentencia = (
        select(CotizacionDolarModel)
        .options(selectinload(CotizacionDolarModel.tipo))
        .where(
          CotizacionDolarModel.tipo_id == tipo_id,
          CotizacionDolarModel.fecha == fecha,
        )
      )
      modelo = session.scalars(sentencia).first()
      return None if modelo is None else _a_cotizacion(modelo)

  def leer_historico_por_tipo(self, tipo_id: int) -> list[CotizacionDolar]:
    """Lee el historico de cotizaciones de un tipo."""
    with self._conexion.obtener_sesion() as session:
      sentencia = (
        select(CotizacionDolarModel)
        .options(selectinload(CotizacionDolarModel.tipo))
        .where(CotizacionDolarModel.tipo_id == tipo_id)
      )
      return [_a_cotizacion(modelo) for modelo in session.scalars(sentencia)]

  def leer_todos(self) -> list[CotizacionDolar]:
    """Lee todas las cotizaciones."""
    with self._conexion.obtener_sesion() as session:
      sentencia = select(CotizacionDolarModel).options(
        selectinload(CotizacionDolarModel.tipo),
      )
      return [_a_cotizacion(modelo) for modelo in session.scalars(sentencia)]

  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Actualiza una cotizacion."""
    clave = (cotizacion.tipo.id, cotizacion.fecha)
    with self._conexion.obtener_sesion() as session:
      if session.get(CotizacionDolarModel, clave) is None:
        raise ValueError("No existe una cotizacion para ese tipo y fecha.")
      session.merge(
        CotizacionDolarModel(
          tipo_id=cotizacion.tipo.id,
          fecha=cotizacion.fecha,
          valor=cotizacion.valor,
        )
      )
    cotizacion_actualizada = self.leer_por_tipo_y_fecha(*clave)
    if cotizacion_actualizada is None:
      raise ValueError("No se pudo recuperar la cotizacion actualizada.")
    return cotizacion_actualizada

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotizacion."""
    with self._conexion.obtener_sesion() as session:
      modelo = session.get(CotizacionDolarModel, (tipo_id, fecha))
      if modelo is None:
        return False
      session.delete(modelo)
      return True
