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

Para ejecutar el proyecto en entorno local se recomienda crear un entorno virtual dentro de la carpeta del proyecto.

Desde la carpeta:

```bash
03_Price_Manager_antolini_martin/
```

crear el entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide la activacion del entorno, ejecutar una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Luego volver a activar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Con el entorno virtual activo, actualizar `pip` e instalar dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verificar que las dependencias principales esten instaladas:

```bash
python -c "import sqlalchemy; print('OK SQLAlchemy')"
python -c "import requests; print('OK requests')"
python -c "import scrapy; print('OK scrapy')"
python -c "import itemloaders; print('OK itemloaders')"
```

El entorno virtual `.venv/` no debe subirse al repositorio.

## Configuracion

Crear un archivo `.env` tomando como referencia `.env.example`:

```env
API_URL=https://dolarapi.com/v1/dolares
```

Tambien se recomienda configurar la variable de entorno `PYTHONPATH` apuntando a la carpeta `src`.

En Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
```

## Ejecucion Local

Desde la carpeta del proyecto, con el entorno virtual activo:

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH="src"
python -m price_manager.main
```

Tambien puede verificarse la importacion de modulos principales:

```powershell
python -c "from price_manager.migrations.migrations import cargar_datos_desde_sql; print('OK migrations')"
python -c "from price_manager.scraper.items import StarComputacionItem; print('OK item')"
python -c "from price_manager.scraper.loaders import StarComputacionLoader; print('OK loader')"
```

## Ejecucion En Google Colab

El notebook de Colab debe clonar el repositorio, seleccionar la rama `Sprint_3`, instalar dependencias y ejecutar las funciones desde `src/price_manager`.

En modo entrega no se requiere `GITHUB_TOKEN` si el repositorio es publico o si el docente ya tiene acceso al repositorio.

```python
!git clone https://github.com/tiburon-blanco/seminario.git
%cd seminario
!git checkout Sprint_3
%cd 03_Price_Manager_antolini_martin
!pip install -r requirements.txt
```

Luego se configura el path del proyecto:

```python
import sys
from pathlib import Path

PROJECT_PATH = Path.cwd()
SRC_PATH = PROJECT_PATH / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

print("PROJECT_PATH:", PROJECT_PATH)
print("SRC_PATH:", SRC_PATH)
```

Finalmente se puede importar y ejecutar el proyecto:

```python
from price_manager.main import main

main(import_default_data=False)
```

Si el repositorio fuera privado, el acceso mediante token debe configurarse en los secretos de Colab, evitando escribir el token directamente en el notebook.

````

## Versionado

El desarrollo del Sprint 3 parte de la rama `Sprint_2` y se realiza en la rama:

```text
Sprint_3
````

La variable `desactivar_git_push` se mantiene en `main.py` para permitir el
traceo requerido por la consigna.

Organizacion del Notebook

El notebook de Colab se encuentra organizado por ejercicios y cada funcionalidad se agrupa en celdas con titulo.

Antes del Ejercicio 01 se incluye una celda de importaciones generales y configuracion inicial. Luego, cada ejercicio contiene celdas de verificacion, prueba controlada y conclusion.

El notebook no reescribe innecesariamente los modulos con %%writefile, porque el codigo fuente se desarrolla y versiona directamente en archivos .py dentro del repositorio. Colab clona la rama Sprint_3 y ejecuta los modulos desde la estructura real del proyecto.

Versionado

El desarrollo del Sprint 3 parte de la rama Sprint_2 y se realiza en la rama:

Sprint_3

La variable desactivar_git_push se mantiene en main.py para permitir el traceo requerido por la consigna.

Archivos generados no versionados

Durante la ejecucion pueden generarse archivos o carpetas temporales:

data/
tmp_ejercicio_02/
price_manager.db
*.sqlite3

Estos archivos son productos de ejecucion y no forman parte del codigo fuente versionado.