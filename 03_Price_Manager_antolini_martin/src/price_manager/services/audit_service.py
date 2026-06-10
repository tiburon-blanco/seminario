"""Servicio y decoradores para auditar operaciones del sistema."""

from __future__ import annotations

import datetime
import functools
import json
from collections.abc import Callable
from typing import Any

from sqlalchemy import select

from price_manager.database.connection import ConexionDB
from price_manager.models.models import AuditoriaModel


def _recortar_texto(valor: str, maximo: int = 500) -> str:
  """Recorta textos largos para guardar detalles legibles."""
  if len(valor) <= maximo:
    return valor

  return valor[:maximo] + "..."


def _serializar_valor(valor: Any) -> str:
  """Convierte un valor cualquiera en texto seguro para auditoria."""
  try:
    texto = repr(valor)
  except Exception:
    texto = f"<{type(valor).__name__}>"

  return _recortar_texto(texto, maximo=250)


def _construir_detalles(
  funcion: Callable[..., Any],
  args: tuple[Any, ...],
  kwargs: dict[str, Any],
  estado: str,
  resultado: Any | None = None,
  error: Exception | None = None,
) -> str:
  """Construye el detalle de una operacion auditada."""
  argumentos = args

  if argumentos and argumentos[0].__class__.__name__.startswith("Servicio"):
    argumentos = argumentos[1:]

  datos = {
    "funcion": funcion.__name__,
    "estado": estado,
    "args": [_serializar_valor(argumento) for argumento in argumentos],
    "kwargs": {
      clave: _serializar_valor(valor)
      for clave, valor in kwargs.items()
    },
  }

  if resultado is not None:
    datos["resultado"] = _serializar_valor(resultado)

  if error is not None:
    datos["error"] = _serializar_valor(error)

  return json.dumps(datos, ensure_ascii=False)


def registrar_auditoria(
  accion: str,
  detalles: str,
  fecha: datetime.datetime | None = None,
) -> None:
  """Registra una auditoria en la base de datos."""
  conexion = ConexionDB()
  conexion.crear_tablas()

  auditoria = AuditoriaModel(
    accion=accion,
    fecha=fecha or datetime.datetime.now(),
    detalles=detalles,
  )

  with conexion.obtener_sesion() as session:
    session.add(auditoria)


def auditar_accion(accion: str | None = None):
  """Decorador para auditar una funcion o metodo del sistema."""

  def decorador(funcion):
    @functools.wraps(funcion)
    def wrapper(*args, **kwargs):
      nombre_accion = accion or funcion.__name__

      try:
        resultado = funcion(*args, **kwargs)

        detalles = _construir_detalles(
          funcion=funcion,
          args=args,
          kwargs=kwargs,
          estado="OK",
          resultado=resultado,
        )

        registrar_auditoria(
          accion=nombre_accion,
          detalles=detalles,
        )

        return resultado

      except Exception as error:
        detalles = _construir_detalles(
          funcion=funcion,
          args=args,
          kwargs=kwargs,
          estado="ERROR",
          error=error,
        )

        registrar_auditoria(
          accion=nombre_accion,
          detalles=detalles,
        )

        raise

    return wrapper

  return decorador


def auditar_clase_servicio(clase):
  """Decorador de clase para auditar todos los metodos publicos."""

  for nombre_atributo, atributo in list(vars(clase).items()):
    if nombre_atributo.startswith("_"):
      continue

    if not callable(atributo):
      continue

    accion = f"{clase.__name__}.{nombre_atributo}"
    metodo_auditado = auditar_accion(accion)(atributo)

    setattr(clase, nombre_atributo, metodo_auditado)

  return clase


def listar_auditorias(limite: int = 20) -> list[dict[str, Any]]:
  """Devuelve las ultimas auditorias registradas."""
  conexion = ConexionDB()
  conexion.crear_tablas()

  with conexion.obtener_sesion() as session:
    sentencia = (
      select(AuditoriaModel)
      .order_by(AuditoriaModel.id.desc())
      .limit(limite)
    )

    registros = session.scalars(sentencia).all()

    return [
      {
        "id": registro.id,
        "accion": registro.accion,
        "fecha": registro.fecha,
        "detalles": registro.detalles,
      }
      for registro in registros
    ]