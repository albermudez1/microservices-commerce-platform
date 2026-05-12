# Pruebas Unitarias - Microservicio de Recomendaciones

## Pruebas Implementadas

Se realizaron pruebas sobre las siguientes funcionalidades:

- Conversión y validación de enteros positivos
- Validación de datos inválidos
- Validación de cuerpos JSON
- Validación de métodos HTTP
- Generación de recomendaciones de productos
- Filtrado de productos sin stock
- Filtrado de productos por precio máximo
- Límite máximo de recomendaciones
- Ordenamiento de productos por cantidad de ventas

En total se implementaron 15 pruebas unitarias utilizando `SimpleTestCase` y `RequestFactory` de Django.

---

## Requisitos

Preparar el entorno:

```bash
python -m venv venv
./venv/Scripts/Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución de las pruebas

Ejecutar todas las pruebas:

```bash
python manage.py test
```

Ejecutar las pruebas con respuesta detallada:

```bash
python manage.py test -v 2
```