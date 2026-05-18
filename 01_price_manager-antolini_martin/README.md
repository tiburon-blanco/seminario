# Price Manager

## Trabajo Práctico Integrador

**Materia:** Seminario de Actualización I
**Carrera:** Licenciatura en Ciencia de Datos
**Integrante:** Antolini Martin

## Sprint actual

### Sprint 1

## Objetivo

El objetivo principal de este proyecto es aplicar los conocimientos adquiridos en
programación orientada a objetos, almacenamiento de datos en archivos para su
persistencia y organización modular de una aplicación desarrollada en Python.

## Introducción y contexto del problema

Una empresa distribuidora de productos electrónicos necesita modernizar su sistema
de gestión de inventarios. Debido a la volatilidad económica, el sistema debe
gestionar precios en diferentes monedas y realizar un seguimiento de la cotización
del dólar para actualizar sus valores de referencia en tiempo real.

En este contexto, se propone desarrollar una aplicación de consola (CLI) robusta
en Python que permita administrar el inventario de un local de hardware, gestionar
productos y stock, registrar cotizaciones del dólar y preparar la base para futuras
comparaciones automáticas de precios con sitios de competencia.

El trabajo simula un entorno de desarrollo real, incremental y colaborativo, en el
que se aplican conceptos de diseño orientado a objetos, persistencia de datos,
modularización del código y control de versiones.

## Alcance funcional del Sprint 1

Durante este sprint se trabajará sobre la inicialización del proyecto, la
configuración del versionado, la organización de la estructura de directorios y la
base del sistema para el desarrollo posterior de la lógica de negocio.

La estructura principal del proyecto es la siguiente:

```text
price_manager/
├── src/
│   └── price_manager/
│       ├── entities/
│       │   └── entities.py
│       ├── preload_data/
│       │   └── preload_data.py
│       ├── repositories/
│       │   └── repositories.py
│       ├── services/
│       │   └── services.py
│       ├── migrations/
│       │   └── csv/
│       │       └── table_name.csv
│       ├── ui/
│       │   └── console.py
│       └── main.py
├── requirements.txt
├── CHANGELOG.md
└── README.md



## Objetivo

El objetivo principal de este proyecto es aplicar los conocimientos adquiridos en programación orientada a objetos, almacenamiento de datos en archivos para su persistencia.



## Introducción y Contexto del problema


### Sprint 1

Una empresa distribuidora de productos electrónicos necesita modernizar su sistema de gestión de inventarios. Debido a la volatilidad económica, el sistema debe gestionar precios en diferentes monedas y seguir de cerca la cotización del dólar para actualizar sus valores en tiempo real.

El objetivo es desarrollar una aplicación de consola (CLI) robusta en Python que permita gestionar el inventario de un local de hardware, cotizar productos en tiempo real según el valor del dólar y comparar precios automáticamente con la competencia web.

Descripción de las Entidades
Para cumplir con el requerimiento, se han identificado las siguientes clases y sus restricciones:

https://books.toscrape.com/

1. Infraestructura de Catálogo y Logística

    - Categoría: Define el rubro de los productos (ej: "Periféricos", "Hardware"). Cada categoría tiene un identificador único numérico y un nombre descriptivo.

    - Proveedor: La entidad que nos provee la mercadería. Se debe registrar su ID, nombre legal y una vía de contacto.

2. Gestión Económica (El módulo crítico)

    - Precio: No es un simple número. Es un objeto que contiene el valor (no puede ser negativo), la moneda (usando el código internacional de 3 letras, ej: ARS, USD) y la fecha de última actualización.

    - CotizaciónDolar: Para proteger la rentabilidad, el sistema debe registrar la cotización diaria. Se debe indicar el valor (siempre positivo), la fecha y el tipo (ej: 'Oficial', 'Blue', 'Bolsa', 'CCL', 'Cripto', 'Tarjeta', 'Mayorista').

3. Núcleo del Negocio

    - Producto: Es el centro del sistema. Cada producto tiene un ID, nombre y descripción. Lo más importante: cada producto está asociado a una instancia de Precio, una Categoría y un Proveedor.

    - Stock: Esta clase vincula un Producto con un Almacén específico, indicando la cantidad disponible (la cual nunca puede ser menor a cero).

El trabajo simulará un entorno de desarrollo real, incremental y colaborativo.
```
