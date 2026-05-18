"""Entidades del dominio para el proyecto Price Manager."""

import datetime


class EntidadBase:
  """Clase base para futuras abstracciones del dominio."""
  pass


class Categoria(EntidadBase):
  """Define el rubro de los productos."""

  def __init__(self, id: int, nombre: str) -> None:
    self.id = id
    self.nombre = nombre

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, valor: int) -> None:
    if valor <= 0:
      raise ValueError("El id de la categoría debe ser mayor a cero.")
    self._id = valor

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, valor: str) -> None:
    valor = valor.strip()
    if not valor:
      raise ValueError("El nombre de la categoría no puede estar vacío.")
    self._nombre = valor

  def __str__(self) -> str:
    return f"Categoria(id={self.id}, nombre='{self.nombre}')"


class Proveedor(EntidadBase):
  """Entidad que provee la mercadería."""

  def __init__(self, id: int, nombre: str, contacto: str) -> None:
    self.id = id
    self.nombre = nombre
    self.contacto = contacto

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, valor: int) -> None:
    if valor <= 0:
      raise ValueError("El id del proveedor debe ser mayor a cero.")
    self._id = valor

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, valor: str) -> None:
    valor = valor.strip()
    if not valor:
      raise ValueError("El nombre del proveedor no puede estar vacío.")
    self._nombre = valor

  @property
  def contacto(self) -> str:
    return self._contacto

  @contacto.setter
  def contacto(self, valor: str) -> None:
    valor = valor.strip()
    if not valor:
      raise ValueError("El contacto no puede estar vacío.")
    self._contacto = valor

  def __str__(self) -> str:
    return (
      f"Proveedor(id={self.id}, nombre='{self.nombre}', "
      f"contacto='{self.contacto}')"
    )


class Moneda(EntidadBase):
  """Representa el tipo de moneda."""

  def __init__(self, id: int, nombre: str) -> None:
    self.id = id
    self.nombre = nombre

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, valor: int) -> None:
    if valor <= 0:
      raise ValueError("El id de la moneda debe ser mayor a cero.")
    self._id = valor

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, valor: str) -> None:
    valor = valor.strip().upper()
    if not valor:
      raise ValueError("El nombre de la moneda no puede estar vacío.")
    self._nombre = valor

  def __str__(self) -> str:
    return f"Moneda(id={self.id}, nombre='{self.nombre}')"


class Precio:
  """Maneja el valor económico y la moneda asociada."""

  def __init__(
    self, valor: float, moneda: Moneda, fecha: datetime.date | None = None
  ) -> None:
    self.valor = valor
    self.moneda = moneda
    self.fecha = fecha or datetime.date.today()

  @property
  def valor(self) -> float:
    return self._valor

  @valor.setter
  def valor(self, nuevo_valor: float) -> None:
    if nuevo_valor < 0:
      raise ValueError("El precio no puede ser negativo.")
    self._valor = float(nuevo_valor)

  @property
  def moneda(self) -> Moneda:
    return self._moneda

  @moneda.setter
  def moneda(self, nueva_moneda: Moneda) -> None:
    if not isinstance(nueva_moneda, Moneda):
      raise ValueError("moneda debe ser una instancia de Moneda.")
    self._moneda = nueva_moneda

  @property
  def fecha(self) -> datetime.date:
    return self._fecha

  @fecha.setter
  def fecha(self, nueva_fecha: datetime.date) -> None:
    if not isinstance(nueva_fecha, datetime.date):
      raise ValueError("fecha debe ser una instancia de datetime.date.")
    self._fecha = nueva_fecha

  def __str__(self) -> str:
    return (
      f"Precio(valor={self.valor}, moneda='{self.moneda.nombre}', "
      f"fecha='{self.fecha}')"
    )


class TipoCotizacion(EntidadBase):
  """Define tipos de dólar: Oficial, Blue, etc."""

  def __init__(self, id: int, nombre: str) -> None:
    self.id = id
    self.nombre = nombre

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, valor: int) -> None:
    if valor <= 0:
      raise ValueError("El id del tipo de cotización debe ser mayor a cero.")
    self._id = valor

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, valor: str) -> None:
    valor = valor.strip()
    if not valor:
      raise ValueError("El nombre del tipo de cotización no puede estar vacío.")
    self._nombre = valor

  def __str__(self) -> str:
    return f"TipoCotizacion(id={self.id}, nombre='{self.nombre}')"


class CotizacionDolar(EntidadBase):
  """Registra el valor diario del dólar por tipo."""

  def __init__(
    self, valor: float, fecha: datetime.date | None = None, tipo: TipoCotizacion | None = None
  ) -> None:
    self.valor = valor
    self.fecha = fecha or datetime.date.today()
    self.tipo = tipo or TipoCotizacion(1, "Oficial")

  @property
  def valor(self) -> float:
    return self._valor

  @valor.setter
  def valor(self, nuevo_valor: float) -> None:
    if nuevo_valor <= 0:
      raise ValueError("La cotización debe ser positiva.")
    self._valor = float(nuevo_valor)

  @property
  def fecha(self) -> datetime.date:
    return self._fecha

  @fecha.setter
  def fecha(self, nueva_fecha: datetime.date) -> None:
    if not isinstance(nueva_fecha, datetime.date):
      raise ValueError("fecha debe ser una instancia de datetime.date.")
    self._fecha = nueva_fecha

  @property
  def tipo(self) -> TipoCotizacion:
    return self._tipo

  @tipo.setter
  def tipo(self, nuevo_tipo: TipoCotizacion) -> None:
    if not isinstance(nuevo_tipo, TipoCotizacion):
      raise ValueError("tipo debe ser una instancia de TipoCotizacion.")
    self._tipo = nuevo_tipo

  def __str__(self) -> str:
    return (
      f"CotizacionDolar(valor={self.valor}, fecha='{self.fecha}', "
      f"tipo='{self.tipo.nombre}')"
    )


class Producto(EntidadBase):
  """Centro del sistema, vincula las entidades principales."""

  def __init__(
    self, id: int, nombre: str, descripcion: str, precio: Precio, categoria: Categoria, proveedor: Proveedor
  ) -> None:
    self.id = id
    self.nombre = nombre
    self.descripcion = descripcion
    self.precio = precio
    self.categoria = categoria
    self.proveedor = proveedor

  @property
  def id(self) -> int:
    return self._id

  @id.setter
  def id(self, valor: int) -> None:
    if valor <= 0:
      raise ValueError("El id del producto debe ser mayor a cero.")
    self._id = valor

  @property
  def nombre(self) -> str:
    return self._nombre

  @nombre.setter
  def nombre(self, valor: str) -> None:
    valor = valor.strip()
    if not valor:
      raise ValueError("El nombre del producto no puede estar vacío.")
    self._nombre = valor

  @property
  def descripcion(self) -> str:
    return self._descripcion

  @descripcion.setter
  def descripcion(self, valor: str) -> None:
    valor = valor.strip()
    if not valor:
      raise ValueError("La descripción no puede estar vacía.")
    self._descripcion = valor

  @property
  def precio(self) -> Precio:
    return self._precio

  @precio.setter
  def precio(self, nuevo_precio: Precio) -> None:
    if not isinstance(nuevo_precio, Precio):
      raise ValueError("precio debe ser una instancia de Precio.")
    self._precio = nuevo_precio

  @property
  def categoria(self) -> Categoria:
    return self._categoria

  @categoria.setter
  def categoria(self, nueva_categoria: Categoria) -> None:
    if not isinstance(nueva_categoria, Categoria):
      raise ValueError("categoria debe ser una instancia de Categoria.")
    self._categoria = nueva_categoria

  @property
  def proveedor(self) -> Proveedor:
    return self._proveedor

  @proveedor.setter
  def proveedor(self, nuevo_proveedor: Proveedor) -> None:
    if not isinstance(nuevo_proveedor, Proveedor):
      raise ValueError("proveedor debe ser una instancia de Proveedor.")
    self._proveedor = nuevo_proveedor

  def __str__(self) -> str:
    return (
      f"Producto(id={self.id}, nombre='{self.nombre}', "
      f"precio={self.precio.valor} {self.precio.moneda.nombre}, "
      f"categoria='{self.categoria.nombre}', "
      f"proveedor='{self.proveedor.nombre}')"
    )


class Stock(EntidadBase):
  """Vincula Producto con cantidad disponible."""

  def __init__(self, producto: Producto, cantidad: int = 0) -> None:
    self.producto = producto
    self.cantidad = cantidad

  @property
  def producto(self) -> Producto:
    return self._producto

  @producto.setter
  def producto(self, nuevo_producto: Producto) -> None:
    if not isinstance(nuevo_producto, Producto):
      raise ValueError("producto debe ser una instancia de Producto.")
    self._producto = nuevo_producto

  @property
  def cantidad(self) -> int:
    return self._cantidad

  @cantidad.setter
  def cantidad(self, nueva_cantidad: int) -> None:
    if nueva_cantidad < 0:
      raise ValueError("El stock no puede ser negativo.")
    self._cantidad = int(nueva_cantidad)

  def __str__(self) -> str:
    return (
      f"Stock(producto='{self.producto.nombre}', "
      f"cantidad={self.cantidad})"
    )
