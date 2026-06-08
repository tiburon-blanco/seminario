# CHANGELOG

## Sprint 3

### Dia 1 - Inicializacion Sprint 3
- Se creo la rama `Sprint_3` partiendo desde `Sprint_2`.
- Se preparo la carpeta `03_Price_Manager_antolini_martin` usando como base el
  proyecto funcional del Sprint 2.
- Se conservaron la estructura modular, la base ORM con SQLAlchemy y el notebook
  de entrega del Sprint 3.
- Se actualizaron dependencias iniciales para scraping y reportes.

### Dia 2 - Carga desde SQL
- Se agrego la funcion `cargar_desde_sql` para ejecutar archivos `.sql` desde la
  carpeta de migraciones.
- Se definio un orden de carga compatible con las claves foraneas del modelo
  relacional.
- Se uso `INSERT OR IGNORE` para evitar duplicados al ejecutar la carga mas de
  una vez.

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
