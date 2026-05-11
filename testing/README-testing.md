# Guía de ejecución de pruebas de rendimiento

## Objetivo

Este documento explica cómo ejecutar la parte de testing del proyecto usando **Locust**, partiendo de la idea de que el sistema ya fue instalado correctamente, con base a las instrucciones de los servicios, y que todos los microservicios ya pueden ejecutarse de forma local.

## Estructura usada para testing

La carpeta `testing/` contiene los archivos usados para las pruebas:

- `setup_test_data.py`: crea los datos mínimos de prueba a través del gateway
- `locustfile.py`: define los endpoints que se prueban con Locust
- `.env.example`: ejemplo de variables de entorno para testing
- `requirements.txt`: dependencias necesarias para la carpeta de testing

## Preparación del entorno virtual

Ubíquese en la carpeta `testing`:

```bash
cd testing
```

Cree el entorno virtual:

```bash
python -m venv venv
```

Actívelo en PowerShell:

```bash
./venv/Scripts/Activate.ps1
```

## Instalación de dependencias

Con el entorno virtual activado, instale las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración del archivo `.env`

Dentro de la carpeta `testing`, cree un archivo `.env` tomando como base `.env.example`.

## Generación de datos de prueba

Antes de ejecutar Locust, se deben generar datos mínimos para el sistema de pruebas.

Este script realiza, a través del gateway, las siguientes acciones:

- registra o reutiliza un usuario de prueba
- inicia sesión
- crea un producto
- crea una tienda
- procesa una venta
- guarda los identificadores generados en `test_data.json`

Ejecute el script así:

```bash
python setup_test_data.py
```

Si todo sale bien, el script generará un archivo `test_data.json` con datos como:

- `user_id`
- `product_id`
- `store_id`
- `sale_id`
- `token`

Este archivo es usado por `locustfile.py` para consumir endpoints con datos válidos.

## Ejecución de Locust

Con el entorno virtual activado y con `test_data.json` ya generado, ejecute:

```bash
locust -f locustfile.py
```

Luego abra en el navegador la interfaz web de Locust:

```text
http://127.0.0.1:8089
```

## Resultados y análisis

Para consultar el análisis completo de las pruebas de rendimiento, revisar el siguiente archivo:

- [Ver análisis de resultados](testing-results-analysis.md)

En ese documento se encuentran:

- la metodología utilizada
- los endpoints evaluados
- los resultados de las pruebas de carga, capacidad y estrés
- los hallazgos generales
- las conclusiones finales