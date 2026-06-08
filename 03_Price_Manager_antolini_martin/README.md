# Price Manager

## Trabajo Practico Integrador

**Materia:** Seminario de Actualizacion I  
**Carrera:** Licenciatura en Ciencia de Datos  
**Grupo:** 10  
**Integrante:** Antolini Martin  
**Repositorio:** https://github.com/tiburon-blanco/seminario.git

## Sprint Actual

### Sprint 3

## Objetivo

El objetivo principal del Sprint 3 es ampliar Price Manager incorporando scraping
web para obtener precios de competidores y compararlos contra los precios internos
del sistema.

La aplicacion parte del Sprint 2, que ya cuenta con persistencia relacional en
SQLite mediante SQLAlchemy, carga inicial desde CSV/SQL, repositorios, servicios y
menu de consola.

## Introduccion y Contexto

Price Manager es una aplicacion de consola para gestionar productos, stock,
cotizaciones y precios. En este sprint se incorpora la consulta de precios web de
Star Computacion para detectar diferencias relevantes frente a los precios propios.

El nuevo alcance permite simular un proceso de monitoreo competitivo: obtener
datos externos, registrar resultados, generar alertas, emitir reportes y auditar
las operaciones realizadas por el sistema.

## Funcionalidades Sprint 3

- Carga de datos iniciales desde archivos SQL.
- Scraper Scrapy para obtener precios y detalles desde Star Computacion.
- Loaders para normalizar datos extraidos.
- Pipelines para persistir resultados del scraping.
- Comparacion entre precio interno y precio web.
- Generacion de alertas CSV segun diferencia maxima ingresada por el usuario.
- Generacion de reporte Excel con precios internos, web y diferencias.
- Auditoria de operaciones mediante decorador.
- Nuevas opciones de menu para scraping, reportes e historial de auditoria.
- Notebook Colab preparado para clonar el repositorio y ejecutar la solucion
  modular desde GitHub.

## Estructura

```text
03_Price_Manager_antolini_martin/
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
│       ├── scraper/
│       │   └── spiders/
│       ├── migrations/
│       │   ├── csv/
│       │   ├── sql/
│       │   └── migrations.py
│       ├── ui/
│       │   └── console.py
│       └── main.py
├── requirements.txt
├── CHANGELOG.md
├── README.md
└── Copia_de_03_Price_Manager_Grupo_X (1).ipynb
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

## Ejecucion Local

Desde la carpeta del proyecto:

```bash
set PYTHONPATH=src
python -m price_manager.main
```

## Ejecucion En Google Colab

El notebook debe clonar el repositorio, seleccionar la rama `Sprint_3`, instalar
dependencias y ejecutar las funciones desde `src/price_manager`.

```python
from google.colab import userdata
GITHUB_TOKEN = userdata.get("GITHUB_TOKEN")
```

```python
!git clone https://$GITHUB_TOKEN@github.com/tiburon-blanco/seminario.git
%cd seminario
!git checkout Sprint_3
%cd 03_Price_Manager_antolini_martin
!pip install -r requirements.txt
```

```python
import sys
sys.path.append("src")

from price_manager.main import main
main(import_default_data=False)
```

## Versionado

El desarrollo del Sprint 3 parte de la rama `Sprint_2` y se realiza en la rama:

```text
Sprint_3
```

La variable `desactivar_git_push` se mantiene en `main.py` para permitir el
traceo requerido por la consigna.
