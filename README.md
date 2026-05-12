# Microservices Commerce Platform (Release #2)

Sistema backend distribuido para una plataforma de comercio, desarrollado con arquitectura de microservicios. El sistema utiliza un API Gateway como único punto de entrada y se compone de servicios para autenticación, catálogo e inventario, ventas, recomendaciones, reportes y cobertura de tiendas.

Toda la infraestructura está **doquerizada y orquestada**, automatizando el despliegue de bases de datos, migraciones y generación de llaves.

## Autor

Alejandro Bermúdez Murcia

## Estructura del proyecto

    microservices-commerce-platform/
    │
    ├── services/
    │   ├── README-services.md
    │   ├── docs/
    │   ├── gateway-laravel/
    │   ├── catalog-inventory-flask/
    │   ├── orders-sales-express/
    │   ├── recommendations-django/
    │   │   ├── README-unit-test.md
    │   │   └── recommendations/
    │   │       └── tests.py
    │   ├── reports-django/
    │   └── coverage-flask/
    │
    ├── testing/
    │   ├── README-testing.md
    │   ├── locustfile.py
    │   ├── setup_test_data.py
    │   ├── testing-results-analysis.md
    │   └── results-images/
    │
    ├── docker-compose.yml
    ├── README.md
    └── .gitignore

---

## Guía de Despliegue y Ejecución (Docker)

### 1. Pre-requisitos
Asegúrese de tener instalado **Docker** y **Docker Compose** en su sistema.

### 2. Configuración de Variables de Entorno
Antes de levantar la infraestructura, es necesario configurar las variables de entorno de los microservicios.
Navegue a las carpetas de los microservicios en `/services`, copie el archivo `.env.example` y renómbrelo como `.env`:

### 3. Levantar la Infraestructura
En la raíz del proyecto (donde se encuentra el `docker-compose.yml`), ejecute el siguiente comando para construir las imágenes y levantar los contenedores en segundo plano:

    docker compose up -d --build

**¡Importante! Automatización:** El sistema está diseñado para que, tras ejecutar este comando, el API Gateway y los microservicios realicen automáticamente la instalación de dependencias, creación de llaves y las migraciones de sus respectivas bases de datos (MySQL, PostgreSQL, MongoDB). Se recomienda esperar entre **15 y 20 segundos** para que todos los procesos internos finalicen y los contenedores estén completamente listos.

El API Gateway quedará expuesto y escuchando peticiones en: `http://localhost:8000/api`

Para mas información de los endpoints consultar:
- [Documentación de endpoints](/services/docs/endpoints.md)

---

## 🧪 Pruebas de Rendimiento (Locust)

Se ha configurado un contenedor específico para realizar pruebas de carga automatizadas. Siga estos pasos para ejecutarlas:

### 1. Generar datos de prueba
Para que Locust tenga información inicial con la cual trabajar (usuarios, productos, tiendas), ejecute el script de preparación de datos dentro del contenedor de testing:

    docker exec locust-testing python setup_test_data.py

*Deberá ver en consola mensajes de éxito (Status: 200/201) indicando que se registraron los usuarios y productos ficticios.*

### 2. Lanzar el motor de Locust
Inicie el servidor de pruebas ejecutando el siguiente comando:

    docker exec locust-testing locust -f locustfile.py --host http://gateway:8000

### 3. Ejecutar la prueba desde el Navegador
1. Abra su navegador web e ingrese a: **http://localhost:8089**
   *(Nota: Aunque la consola de Docker muestre `http://0.0.0.0:8089`, debe utilizar `localhost` para acceder desde su máquina host).*
2. Para ver los resultados de las pruebas realizadas puede consultar:
- [Análisis de resultados](/testing/testing-results-analysis.md)

---

## Documentación de microservicios

La documentación detallada relacionada con la arquitectura, despliegue, rutas de API y funcionamiento de cada microservicio se encuentra en:

- [Documentación de servicios](services/README-services.md)

---

## Pruebas unitarias

Las pruebas unitarias fueron implementadas en el microservicio `recommendations-django`.

- [Documentación de pruebas unitarias](services/recommendations-django/README-unit-tests.md)

---

## Pruebas de rendimiento

Las pruebas de rendimiento fueron desarrolladas utilizando Locust y se encuentran en la carpeta `testing`.

- [Documentación y Análisis de pruebas de rendimiento](testing/README-testing.md)