# Microservices Commerce Platform (Release #1)

Sistema backend distribuido para una plataforma de comercio, desarrollado con arquitectura de microservicios. El sistema utiliza un API Gateway como único punto de entrada y se compone de servicios para autenticación, catálogo e inventario, ventas, recomendaciones, reportes y cobertura de tiendas.

## Autor

Alejandro Bermúdez Murcia

## Tecnologías utilizadas

* PHP 8.3.16
* Composer 2.8.9
* Python 3.13.3
* Node.js 22.15.0
* npm 10.9.2
* MongoDB Server 8.2.5
* MongoDB Shell 2.7.0
* PostgreSQL 18.3
* MySQL vía Laragon
* Laravel
* Flask
* Express
* Django

## Bases de datos utilizadas

* **MySQL**: gateway, catálogo/inventario, cobertura de tiendas y reportes
* **MongoDB**: ventas
* **PostgreSQL**: recomendaciones

## Estructura del proyecto

```bash
microservices-commerce-platform/
│
├── services/
│   ├── gateway-laravel/
│   ├── catalog-inventory-flask/
│   ├── orders-sales-express/
│   ├── recommendations-django/
│   ├── reports-django/
│   └── coverage-flask/
│
└── docs/
```

## Descripción general de la arquitectura

* **API Gateway (Laravel)** es el único punto de entrada para el cliente.
* Todas las peticiones externas pasan por el gateway.
* La comunicación interna entre gateway y microservicios está protegida por `X-Gateway-Token`.
* El flujo principal del sistema es el procesamiento de ventas:

  1. autenticación del usuario
  2. consulta del producto
  3. validación de stock
  4. registro de la venta
  5. actualización del inventario
* Los demás microservicios complementan el sistema con recomendaciones, reportes y cobertura de tiendas.

## Requisitos previos

Antes de ejecutar el proyecto, se debe tener instalado:

* PHP 8.3.16
* Composer 2.8.9
* Python 3.13.3
* Node.js 22.15.0
* npm 10.9.2
* MongoDB Server 8.2.5
* MongoDB Shell 2.7.0
* PostgreSQL 18.3
* Laragon 8.1 con MySQL habilitado

Además:

* **MySQL** debe estar corriendo (Laragon)
* **PostgreSQL** debe estar corriendo
* **MongoDB** debe iniciarse manualmente con `mongod`

## Instalación y ejecución del proyecto

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd microservices-commerce-platform
```

### 2. Levantar MongoDB

Abrir una terminal y ejecutar:

```bash
mongod
```

### 3. Ejecutar el API Gateway (Laravel)

Abrir una nueva terminal:

```bash
cd services/gateway-laravel
composer install
php artisan key:generate
php artisan migrate
php artisan serve --host=127.0.0.1 --port=8000
```

URL base del gateway:

```text
http://127.0.0.1:8000
```

### 4. Ejecutar el microservicio de Catálogo e Inventario (Flask)

Abrir una nueva terminal:

```bash
cd services/catalog-inventory-flask
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
flask db upgrade
flask --app app.py run --host=127.0.0.1 --port=5001
```

URL del servicio:

```text
http://127.0.0.1:5001
```

### 5. Ejecutar el microservicio de Ventas (Express)

Abrir una nueva terminal:

```bash
cd services/orders-sales-express
npm install
node index.js
```

URL del servicio:

```text
http://127.0.0.1:3000
```

### 6. Ejecutar el microservicio de Recomendaciones (Django)

Abrir una nueva terminal:

```bash
cd services/recommendations-django
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8001
```

URL del servicio:

```text
http://127.0.0.1:8001
```

### 7. Ejecutar el microservicio de Reportes (Django)

Abrir una nueva terminal:

```bash
cd services/reports-django
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8002
```

URL del servicio:

```text
http://127.0.0.1:8002
```

### 8. Ejecutar el microservicio de Cobertura de Tiendas (Flask)

Abrir una nueva terminal:

```bash
cd services/coverage-flask
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
flask db upgrade
flask --app app.py run --host=127.0.0.1 --port=5002
```

URL del servicio:

```text
http://127.0.0.1:5002
```

## Puertos utilizados

* Gateway Laravel: `8000`
* Catálogo e Inventario Flask: `5001`
* Ventas Express: `3000`
* Recomendaciones Django: `8001`
* Reportes Django: `8002`
* Cobertura de Tiendas Flask: `5002`

## Flujo principal del sistema

El flujo principal del negocio funciona a través del API Gateway:

1. El usuario se autentica en el gateway.
2. El usuario envía una solicitud para procesar una venta.
3. El gateway consulta el producto en catálogo/inventario.
4. El gateway valida el stock disponible.
5. El gateway registra la venta en el microservicio de ventas.
6. El gateway actualiza el stock en catálogo/inventario.
7. El gateway devuelve una respuesta consolidada.

## Documentación adicional

La documentación detallada del proyecto se encuentra en la carpeta `docs/`:

* `architecture.md`
* `flow.md`
* `endpoints.md`
