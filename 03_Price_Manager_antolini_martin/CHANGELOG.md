# CHANGELOG

## Sprint 3

### Dia 1 - Inicializacion Sprint 3

- Se creo la rama `Sprint_3` partiendo desde `Sprint_2`.
- Se preparo la carpeta `03_Price_Manager_antolini_martin` usando como base el
  proyecto funcional del Sprint 2.
- Se conservaron la estructura modular, la base ORM con SQLAlchemy y el notebook
  de entrega del Sprint 3.
- Se agrego la estructura inicial requerida para scraping:
  - `src/price_manager/scraper/`
  - `src/price_manager/scraper/spiders/`

- Se actualizaron dependencias iniciales para scraping y reportes.
- Se preparo el notebook Colab para clonar el repositorio, seleccionar la rama
  `Sprint_3` y configurar `PYTHONPATH`.

### Dia 2 - Carga desde SQL

- Se agrego la funcion `cargar_datos_desde_sql` para ejecutar archivos `.sql`
  individuales.
- Se agrego la funcion `cargar_desde_sql` para ejecutar archivos `.sql` desde la
  carpeta de migraciones.
- Se definio un orden de carga compatible con las claves foraneas del modelo
  relacional.
- Se valido la existencia del archivo SQL antes de ejecutarlo.
- Se valido que el archivo tenga extension `.sql`.
- Se uso `INSERT OR IGNORE` para evitar duplicados al ejecutar la carga mas de
  una vez.
- Se verifico la correcta compilacion e importacion del modulo `migrations.py`.
- Se agregaron celdas en Colab para probar la carga desde SQL de forma
  controlada.

### Dia 3 - Scraper StarComputacionSpider

- Se creo el modulo `scraper` dentro del paquete `price_manager`.
- Se implemento el spider `StarComputacionSpider` utilizando Scrapy.
- Se limito la busqueda a productos propios del sistema.
- Se configuro el limite de 10 resultados por busqueda.
- Se extrajeron los siguientes datos desde la web:
  - Precio.
  - URL de imagen.
  - Formas de pago.
  - Precio asociado a formas de pago.
  - Descripcion detallada.
  - URL del producto.
  - Fuente de extraccion.

- Se implemento `StarComputacionItem` para estructurar los datos extraidos.
- Se implemento `StarComputacionLoader` para limpiar y normalizar textos,
  precios y descripciones.
- Se implementaron pipelines para:
  - Validar datos minimos.
  - Evitar duplicados por URL.
  - Guardar resultados en formato JSON Lines.

- Se agrego configuracion propia del scraper en `settings.py`.
- Se creo `runner.py` para ejecutar el scraper desde Python o desde Colab.
- Se actualizaron las dependencias del proyecto incorporando Scrapy e
  ItemLoaders.
- Se agrego una prueba controlada en Colab con HTML simulado para validar el
  funcionamiento sin depender de un sitio externo.
- Se dejo una ejecucion real opcional del scraper para evitar que el notebook
  dependa obligatoriamente de la disponibilidad de la pagina web.

### Dia 4 - Comparacion de precios y alertas

- Se creo el servicio `price_alert_service.py`.
- Se implemento la comparacion entre precio interno y precio web.
- Se agrego una funcion para extraer precios numericos desde textos con formato
  monetario.
- Se permitio ingresar por usuario la diferencia maxima permitida antes de la
  ejecucion.
- Se calcularon los siguientes datos:
  - Precio interno.
  - Precio web.
  - Diferencia en monto.
  - Diferencia porcentual.
  - Indicador de alerta.

- Se genero un archivo CSV de alertas para analizar diferencias de precios.
- Se preparo el CSV para ser descargado desde Colab.
- Se agrego una ejecucion real opcional integrada con el scraper.
- Se dejo una prueba controlada para que el notebook pueda ejecutarse completo
  sin depender de la disponibilidad del sitio externo.

### Dia 5 - Reporte Excel de precios

- Se creo el servicio `excel_report_service.py`.
- Se implemento la generacion de reportes Excel utilizando `openpyxl`.
- Se genero un archivo `.xlsx` con los campos requeridos:
  - Producto.
  - Precio interno.
  - Precio web.
  - Diferencia.
  - Fecha de extraccion.

- Se incorporo formato basico al archivo Excel:
  - Encabezados destacados.
  - Ajuste automatico de ancho de columnas.
  - Formato monetario en columnas de precios.

- Se integro la lectura de resultados generados por el scraper.
- Se reutilizo la logica de comparacion de precios del servicio de alertas.
- Se agrego la posibilidad de descargar el reporte Excel desde Colab.
- Se dejo una ejecucion real opcional integrada con el scraper.

### - Documentacion y configuracion final

- Se actualizo el archivo `README.md` con la descripcion del Sprint 3.
- Se actualizo el archivo `CHANGELOG.md` con el detalle de los ejercicios
  realizados.
- Se actualizaron las dependencias en `requirements.txt`.
- Se agrego configuracion en `.gitignore` para excluir entorno virtual, archivos
  temporales, bases locales y carpetas de datos generadas.
- Se mantuvo la separacion entre desarrollo real en VS Code y verificacion
  reproducible en Google Colab.
- Se verifico que el proyecto pueda ser ejecutado desde Colab clonando la rama
  `Sprint_3`.

  ### Dia 6 - Auditoria del sistema

* Se agrego la tabla `auditorias` al modelo ORM del sistema.
* La tabla de auditoria registra los campos requeridos:
  - Accion.
  - Fecha.
  - Detalles.

* Se incorporo el modelo `AuditoriaModel` en `models.py`.
* Se creo el servicio `audit_service.py` para centralizar la logica de auditoria.
* Se implemento la funcion `registrar_auditoria` para guardar registros de auditoria en la base de datos.
* Se implemento el decorador `@auditar_accion` para auditar funciones y metodos del sistema.
* Se implemento el decorador de clase `@auditar_clase_servicio` para auditar automaticamente los metodos publicos de los servicios.
* Se agrego la funcion `listar_auditorias` para consultar los ultimos registros generados.
* Se modificaron los servicios principales para registrar auditorias en las operaciones del sistema.
* Se incorporo auditoria en operaciones relacionadas con:
  - Migraciones y carga desde SQL.
  - Ejecucion del scraper.
  - Lectura de resultados JSON Lines.
  - Generacion de alertas CSV.
  - Generacion de reportes Excel.

* Se verifico la correcta importacion del modelo `AuditoriaModel`.
* Se verifico la correcta importacion del servicio de auditoria.
* Se realizo una prueba manual de registro de auditoria.
* Se preparo una prueba del decorador para validar que una funcion auditada genere registros automaticamente.

### Dia 7 - Opciones de menu Sprint 3

- Se modifico el menu principal del sistema para integrar funcionalidades del Sprint 3.
- Se agrego la opcion `Ejecutar scraping`.
- Se agrego la opcion `Generar reporte`.
- Se agrego la opcion `Ver historial de auditoria`.
- Se vinculo la opcion de scraping con la ejecucion del `StarComputacionSpider`.
- Se configuro la ejecucion del scraper con un limite de 10 resultados por busqueda.
- Se genero el archivo de resultados web en formato JSON Lines.
- Se vinculo la opcion de reporte con la generacion del archivo Excel de comparacion de precios.
- Se incorporo la consulta del historial de auditorias desde el menu de consola.
- Se permitio visualizar las ultimas auditorias registradas con:
  - ID.
  - Accion.
  - Fecha.
  - Detalles.

- Se verifico que las opciones requeridas por la consigna se encuentren disponibles en la interfaz de consola.

## Sprint 1

### Dia 1 - Inicializacion y estructura base

- Se creo la estructura inicial del proyecto.
- Se agregaron `README.md`, `CHANGELOG.md` y `requirements.txt`.
- Se incorporo la variable `desactivar_git_push` en `main.py`.

### Dia 2 - Definicion de entidades

- Se implementaron las clases del dominio en `entities.py`.
- Se definieron entidades para categorias, proveedores, monedas, precios,
  tipos de cotizacion, cotizaciones, productos y stock.
- Se aplico encapsulamiento mediante propiedades y setters.

### Dia 3 - Persistencia y CRUD en memoria

- Se implementaron repositorios CRUD en memoria.
- Se agregaron repositorios especificos para stock y cotizaciones.

### Dia 4 - Logica de negocio

- Se implementaron servicios para categorias, proveedores, productos, stock y
  cotizaciones.
- Se agregaron validaciones de negocio sobre duplicados y existencia previa.

### Dia 5 - Archivos CSV

- Se crearon archivos CSV dentro de `migrations/csv`.
- Se incorporaron registros iniciales para las entidades principales.

### Dia 6 - Interfaz de usuario

- Se implemento el menu CLI del sistema.
- Se conecto la interfaz con la capa de servicios.

### Dia 7 - Punto de entrada

- Se implemento `main.py` como punto de entrada principal.

### Dia 8 - Precarga de datos

- Se implemento `preload_data.py` para cargar datos desde CSV.

## Sprint 2

### Dia 1 - Rama y estructura Sprint 2

- Se creo la rama `Sprint_2` partiendo de `sprint1`.
- Se creo la carpeta `02_price_manager-antolini_martin`.
- Se copio la base funcional del Sprint 1 evitando archivos generados.
- Se agrego `.gitignore` para excluir `.env`, bases SQLite, cache y archivos de
  Colab.

### Dia 2 - Conexion SQLAlchemy

- Se agrego `database/connection.py`.
- Se implemento la clase `ConexionDB`.
- Se agrego un context manager para manejar sesiones, commit, rollback y cierre.

### Dia 3 - Modelos relacionales

- Se agrego `models/models.py`.
- Se definieron tablas para categorias, proveedores, monedas, tipos de
  cotizacion, productos, stock y cotizaciones del dolar.
- Se configuraron claves primarias, claves foraneas y relaciones ORM.

### Dia 4 - Migracion de datos

- Se implemento `migrations/migrations.py`.
- Se migro la informacion inicial desde CSV hacia SQLite.
- Se generaron archivos `.sql` con sentencias `INSERT` para cada tabla.

### Dia 5 - Repositorios con base de datos

- Se reemplazaron los repositorios en memoria por repositorios SQLAlchemy.
- Se mantuvo la interfaz CRUD usada por los servicios del Sprint 1.
- Se agrego conversion entre modelos ORM y entidades del dominio.

### Dia 6 - Servicios y API del dolar

- Se agrego `obtener_cotizaciones` en `ServicioCotizacionDolar`.
- Se incorporo lectura de `API_URL` desde `.env` mediante `python-dotenv`.
- Se agrego registro y actualizacion de cotizaciones obtenidas por API.

### Dia 7 - Menu y exportacion

- Se agregaron opciones al menu para consultar cotizaciones por API.
- Se incorporo la visualizacion de lista de precios bimonetaria.
- Se agrego exportacion de precios a CSV para cotizaciones disponibles.

### Dia 8 - Documentacion y validacion

- Se actualizo `README.md` con objetivo, contexto, instalacion y ejecucion.
- Se actualizo `CHANGELOG.md` con los cambios del Sprint 2.
- Se valido la carga inicial de productos y cotizaciones desde la base de datos.
