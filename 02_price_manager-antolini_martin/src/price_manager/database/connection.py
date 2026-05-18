"""Conexion y manejo transaccional de la base de datos."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from price_manager.models.models import Base


class ConexionDB:
  """Administra el engine, las sesiones y la creacion de tablas."""

  def __init__(self, url_db: str = "sqlite:///price_manager.db") -> None:
    self.url_db = url_db
    self.engine = create_engine(self.url_db, echo=False, future=True)
    self.SessionLocal = sessionmaker(
      bind=self.engine,
      autoflush=False,
      autocommit=False,
      expire_on_commit=False,
    )

  def crear_tablas(self) -> None:
    """Crea las tablas declaradas en los modelos si no existen."""
    Base.metadata.create_all(self.engine)

  @contextmanager
  def obtener_sesion(self) -> Iterator[Session]:
    """Abre una sesion y controla commit, rollback y cierre."""
    session = self.SessionLocal()
    try:
      yield session
      session.commit()
    except Exception:
      session.rollback()
      raise
    finally:
      session.close()


conexion_db = ConexionDB()
