"""Clases responsables de la persistencia de datos del sistema."""

import abc
import csv
import os
import datetime
from typing import Generic, List, Optional, TypeVar
from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  EntidadBase,
  Moneda,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz genérica para repositorios con operaciones CRUD."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    """Crea una entidad en el repositorio."""
    pass

  @abc.abstractmethod
  def leer_por_id(self, id_entidad: int) -> Optional[T]:
    """Busca una entidad por su identificador."""
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    """Devuelve todas las entidades almacenadas."""
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente."""
    pass

  @abc.abstractmethod
  def eliminar(self, id_entidad: int) -> bool:
    """Elimina una entidad por su identificador."""
    pass


class IRepositorioStock(abc.ABC):
  """Interfaz para persistir registros de stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    """Crea un registro de stock."""
    pass

  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    """Busca un stock por id de producto."""
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[Stock]:
    """Devuelve todos los registros de stock."""
    pass

  @abc.abstractmethod
  def actualizar(self, stock: Stock) -> Stock:
    """Actualiza un registro de stock."""
    pass

  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool:
    """Elimina un registro de stock por id de producto."""
    pass


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz para persistir cotizaciones de dólar."""

  @abc.abstractmethod
  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Crea una cotización."""
    pass

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(
    self,
    tipo_id: int,
    fecha: datetime.date
  ) -> Optional[CotizacionDolar]:
    """Busca una cotización por tipo y fecha."""
    pass

  @abc.abstractmethod
  def leer_historico_por_tipo(
    self,
    tipo_id: int
  ) -> List[CotizacionDolar]:
    """Devuelve el histórico de un tipo de cotización."""
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[CotizacionDolar]:
    """Devuelve todas las cotizaciones."""
    pass

  @abc.abstractmethod
  def actualizar(
    self,
    cotizacion: CotizacionDolar
  ) -> CotizacionDolar:
    """Actualiza una cotización existente."""
    pass

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotización por tipo y fecha."""
    pass


class RepositorioEnMemoria(IRepositorio[T]):
  """Implementación genérica de un repositorio en memoria."""

  def __init__(self) -> None:
    self._datos: dict[int, T] = {}

  def crear(self, entidad: T) -> T:
    """Crea una entidad si su id no existe."""
    if entidad.id in self._datos:
      raise ValueError(f"Ya existe una entidad con id {entidad.id}.")
    self._datos[entidad.id] = entidad
    return entidad

  def leer_por_id(self, id_entidad: int) -> Optional[T]:
    """Busca una entidad por id."""
    return self._datos.get(id_entidad)

  def leer_todos(self) -> List[T]:
    """Devuelve todas las entidades almacenadas."""
    return list(self._datos.values())

  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente."""
    if entidad.id not in self._datos:
      raise ValueError(f"No existe una entidad con id {entidad.id}.")
    self._datos[entidad.id] = entidad
    return entidad

  def eliminar(self, id_entidad: int) -> bool:
    """Elimina una entidad por id."""
    if id_entidad in self._datos:
      del self._datos[id_entidad]
      return True
    return False


class RepositorioCategoria(RepositorioEnMemoria[Categoria]):
  """Repositorio en memoria para categorías."""
  pass


class RepositorioProveedor(RepositorioEnMemoria[Proveedor]):
  """Repositorio en memoria para proveedores."""
  pass


class RepositorioMoneda(RepositorioEnMemoria[Moneda]):
  """Repositorio en memoria para monedas."""
  pass


class RepositorioTipoCotizacion(RepositorioEnMemoria[TipoCotizacion]):
  """Repositorio en memoria para tipos de cotización."""
  pass


class RepositorioProducto(RepositorioEnMemoria[Producto]):
  """Repositorio en memoria para productos."""
  pass


class RepositorioStock(IRepositorioStock):
  """Repositorio en memoria para registros de stock."""

  def __init__(self) -> None:
    self._datos: dict[int, Stock] = {}

  def crear(self, stock: Stock) -> Stock:
    """Crea un stock usando como clave el id del producto."""
    producto_id = stock.producto.id
    if producto_id in self._datos:
      raise ValueError(
        f"Ya existe un stock para el producto con id {producto_id}."
      )
    self._datos[producto_id] = stock
    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    """Busca un stock por id de producto."""
    return self._datos.get(producto_id)

  def leer_todos(self) -> List[Stock]:
    """Devuelve todos los registros de stock."""
    return list(self._datos.values())

  def actualizar(self, stock: Stock) -> Stock:
    """Actualiza un stock existente."""
    producto_id = stock.producto.id
    if producto_id not in self._datos:
      raise ValueError(
        f"No existe stock para el producto con id {producto_id}."
      )
    self._datos[producto_id] = stock
    return stock

  def eliminar(self, producto_id: int) -> bool:
    """Elimina un stock por id de producto."""
    if producto_id in self._datos:
      del self._datos[producto_id]
      return True
    return False


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  """Repositorio en memoria para cotizaciones de dólar."""

  def __init__(self) -> None:
    self._datos: dict[tuple[int, datetime.date], CotizacionDolar] = {}

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """Crea una cotización usando tipo y fecha como clave."""
    clave = (cotizacion.tipo.id, cotizacion.fecha)
    if clave in self._datos:
      raise ValueError("Ya existe una cotización para ese tipo y fecha.")
    self._datos[clave] = cotizacion
    return cotizacion

  def leer_por_tipo_y_fecha(
    self,
    tipo_id: int,
    fecha: datetime.date
  ) -> Optional[CotizacionDolar]:
    """Busca una cotización por tipo y fecha."""
    return self._datos.get((tipo_id, fecha))

  def leer_historico_por_tipo(
    self,
    tipo_id: int
  ) -> List[CotizacionDolar]:
    """Devuelve todas las cotizaciones de un tipo."""
    return [
      cotizacion
      for (id_tipo, _), cotizacion in self._datos.items()
      if id_tipo == tipo_id
    ]

  def leer_todos(self) -> List[CotizacionDolar]:
    """Devuelve todas las cotizaciones."""
    return list(self._datos.values())

  def actualizar(
    self,
    cotizacion: CotizacionDolar
  ) -> CotizacionDolar:
    """Actualiza una cotización existente."""
    clave = (cotizacion.tipo.id, cotizacion.fecha)
    if clave not in self._datos:
      raise ValueError("No existe una cotización para ese tipo y fecha.")
    self._datos[clave] = cotizacion
    return cotizacion

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotización por tipo y fecha."""
    clave = (tipo_id, fecha)
    if clave in self._datos:
      del self._datos[clave]
      return True
    return False
