# Price Manager

## Trabajo Practico Integrador

**Materia:** Seminario de Actualizacion I  
**Carrera:** Licenciatura en Ciencia de Datos  
**Grupo:** 10  
**Integrante:** Antolini Martin  
**Repositorio:** https://github.com/tiburon-blanco/seminario.git

## Sprint Actual

### Sprint 2

## Objetivo

El objetivo principal del Sprint 2 es migrar el sistema Price Manager desde una
persistencia basada en archivos CSV y repositorios en memoria hacia una base de
datos relacional administrada con SQLAlchemy.

El sprint tambien incorpora la consulta a una API externa de cotizaciones del
dolar, la carga inicial automatica, la generacion de scripts SQL de migracion y
nuevas opciones de menu para visualizar y exportar precios bimonetarios.

## Introduccion y Contexto

Price Manager es una aplicacion de consola para gestionar productos de un local
stock y cotizaciones del dolar.

En el Sprint 1 se implementaron las entidades del dominio, los repositorios en
memoria, la precarga desde CSV, los servicios de negocio y el menu CLI. En este
Sprint 2 se consolida la persistencia relacional para simular un escenario mas
cercano a un sistema real, donde los datos sobreviven entre ejecuciones y pueden
consultarse mediante modelos ORM.

## Funcionalidades

- Conexion a base de datos SQLite mediante SQLAlchemy.
- Context manager transaccional para sesiones de base de datos.
- Modelos relacionales para categorias, proveedores, monedas, tipos de
  cotizacion, productos, stock y cotizaciones del dolar.
- Migracion desde archivos CSV a tablas relacionales.
- Generacion de archivos `.sql` con sentencias `INSERT`.
- Repositorios CRUD respaldados por base de datos.
- Consulta de cotizaciones desde `https://dolarapi.com/v1/dolares`.
- Visualizacion de lista de precios en pesos y moneda seleccionada.
- Exportacion de precios a CSV para tipos de moneda/cotizacion disponibles.

## Estructura

```text
02_price_manager-antolini_martin/
├── src/
│   └── price_manager/
│       ├── database/
│       │   └── connection.py
│       ├── entities/
│       │   └── entities.py
│       ├── models/
│       │   └── models.py
│       ├── preload_data/
│       │   └── preload_data.py
│       ├── repositories/
│       │   └── repositories.py
│       ├── services/
│       │   └── services.py
│       ├── migrations/
│       │   ├── csv/
│       │   ├── sql/
│       │   └── migrations.py
│       ├── ui/
│       │   └── console.py
│       └── main.py
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

## Instalacion

```bash
pip install -r requirements.txt
```

## Configuracion

Crear un archivo `.env` tomando como referencia `.env.example`:

```env
API_URL=https://dolarapi.com/v1/dolares
```

## Ejecucion

Desde la carpeta del proyecto:

```bash
set PYTHONPATH=src
python -m price_manager.main
```

En Google Colab, posicionarse en la carpeta `src` y ejecutar:

```python
from price_manager.main import main
main(import_default_data=False)
```

## Versionado

El desarrollo del Sprint 2 parte de la rama `sprint1` y se realiza en la rama:

```text
Sprint_2
```

La variable `desactivar_git_push` se mantiene en `main.py` para permitir
