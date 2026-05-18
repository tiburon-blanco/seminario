# CHANGELOG

## Día 1 - Inicialización y estructura base
- Se creó el repositorio en GitLab.
- Se invitó a los docentes como colaboradores.
- Se clonó el proyecto en entorno local.
- Se generó la estructura base de carpetas.
- Se crearon los archivos principales del sistema.
- Se agregaron `README.md`, `CHANGELOG.md` y `requirements.txt`.
- Se incorporó la variable `desactivar_git_push` en `main.py`.

## Día 2 - Definición de entidades
- Se implementaron las clases del dominio en `entities.py`.
- Se definieron las entidades:
  - `Categoria`
  - `Proveedor`
  - `Moneda`
  - `Precio`
  - `TipoCotizacion`
  - `CotizacionDolar`
  - `Producto`
  - `Stock`
- Se aplicó encapsulación mediante propiedades y setters.
- Se agregaron validaciones básicas sobre ids, nombres, cantidades y valores.
- Se modelaron relaciones entre objetos del dominio.

## Día 3 - Persistencia y CRUD
- Se implementaron las clases responsables de la persistencia en `repositories.py`.
- Se definió una interfaz genérica `IRepositorio` con operaciones CRUD.
- Se implementó `RepositorioEnMemoria` como base genérica para entidades con identificador.
- Se crearon repositorios concretos para:
  - `Categoria`
  - `Proveedor`
  - `Moneda`
  - `TipoCotizacion`
  - `Producto`
- Se implementaron repositorios especiales para:
  - `Stock`
  - `CotizacionDolar`
- Se realizaron pruebas de creación, lectura, actualización y eliminación.
- El objeto `Precio` se mantiene como parte de `Producto`, por lo que no se implementó un repositorio independiente para esa clase.

## Día 4 - Lógica de negocio
- Se implementaron las clases responsables de la lógica del sistema en `services.py`.
- Se desarrollaron servicios para:
  - `Categoria`
  - `Proveedor`
  - `Producto`
  - `Stock`
  - `CotizacionDolar`
- Se aplicaron validaciones de negocio, como control de duplicados y verificación de existencia previa.
- Se integraron entidades y repositorios mediante la capa de servicios.
- Se realizaron pruebas funcionales de creación, lectura, actualización y eliminación.

## Día 5 - Archivos de importación CSV
- Se crearon archivos CSV dentro de `migrations/csv`.
- Se incorporaron registros iniciales para:
  - `Categoria`
  - `Proveedor`
  - `Moneda`
  - `TipoCotizacion`
  - `Producto`
  - `Stock`
  - `CotizacionDolar`
- Cada clase cuenta con un mínimo de 10 registros para importación de datos.

## Día 6 - Interfaz de usuario
- Se implementó la interfaz de usuario del sistema en `console.py`.
- Se desarrollaron menús de operación para:
  - `Categoria`
  - `Proveedor`
  - `Producto`
  - `Stock`
  - `CotizacionDolar`
- La interfaz quedó conectada con la capa de servicios para operar con el CRUD.
- Se incorporó la precarga de datos para facilitar la inicialización del sistema.
- Se validó la correcta importación e instanciación de la clase `ConsolaPriceManager`.

## Día 7 - Punto de entrada principal
- Se implementó el punto de entrada principal del sistema en `main.py`.
- Se vinculó `main.py` con la interfaz de usuario definida en `console.py`.
- Se mantuvo la variable `desactivar_git_push` solicitada por la consigna.
- Se definió la función `main()` para lanzar la aplicación.
- Se verificó la correcta importación y compilación del punto de entrada principal.

## Día 8 - Precarga de datos
- Se implementó `preload_data.py` para la lectura de archivos CSV.
- Se desarrolló la función `precargar_datos()` para inicializar repositorios desde `migrations/csv`.
- Se incorporó la lectura y carga de:
  - `Categoria`
  - `Proveedor`
  - `Moneda`
  - `TipoCotizacion`
  - `Producto`
  - `Stock`
  - `CotizacionDolar`
- Se dejó preparada una celda de precarga de datos en el notebook para evitar carga manual.
