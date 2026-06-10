"""Modelos relacionales del sistema Price Manager."""

import datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  """Base declarativa para los modelos ORM."""


class CategoriaModel(Base):
  """Tabla de categorias de productos."""

  __tablename__ = "categorias"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)


class ProveedorModel(Base):
  """Tabla de proveedores."""

  __tablename__ = "proveedores"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
  contacto: Mapped[str] = mapped_column(String(120), nullable=False)


class MonedaModel(Base):
  """Tabla de monedas."""

  __tablename__ = "monedas"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)


class TipoCotizacionModel(Base):
  """Tabla de tipos de cotizacion."""

  __tablename__ = "tipos_cotizacion"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)


class ProductoModel(Base):
  """Tabla de productos con su precio actual."""

  __tablename__ = "productos"

  __table_args__ = (UniqueConstraint("nombre"),)

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(120), nullable=False)
  descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
  precio_valor: Mapped[float] = mapped_column(Float, nullable=False)
  moneda_id: Mapped[int] = mapped_column(ForeignKey("monedas.id"))
  precio_fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False)
  categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
  proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))

  moneda: Mapped[MonedaModel] = relationship()
  categoria: Mapped[CategoriaModel] = relationship()
  proveedor: Mapped[ProveedorModel] = relationship()


class StockModel(Base):
  """Tabla de stock por producto."""

  __tablename__ = "stock"

  producto_id: Mapped[int] = mapped_column(
    ForeignKey("productos.id"),
    primary_key=True,
  )
  cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

  producto: Mapped[ProductoModel] = relationship()


class CotizacionDolarModel(Base):
  """Tabla de cotizaciones del dolar por tipo y fecha."""

  __tablename__ = "cotizaciones_dolar"

  tipo_id: Mapped[int] = mapped_column(
    ForeignKey("tipos_cotizacion.id"),
    primary_key=True,
  )
  fecha: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
  valor: Mapped[float] = mapped_column(Float, nullable=False)

  tipo: Mapped[TipoCotizacionModel] = relationship()
  
class AuditoriaModel(Base):
  """Tabla de auditoria del sistema."""

  __tablename__ = "auditorias"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  accion: Mapped[str] = mapped_column(String(120), nullable=False)
  fecha: Mapped[datetime.datetime] = mapped_column(
    DateTime,
    nullable=False,
    default=datetime.datetime.now,
  )
  detalles: Mapped[str] = mapped_column(Text, nullable=False)
