# Documentación de endpoints

## Descripción general

Todos los endpoints del sistema deben consumirse a través del **Laravel Gateway**.

URL base del gateway:

```text
http://127.0.0.1:8000/api
```

Los microservicios internos de Flask, Express y Django no deben ser consumidos directamente por el cliente.

## Autenticación requerida

Los endpoints del sistema se dividen en dos grupos:

### Endpoints públicos

No requieren autenticación:

* `POST /register`
* `POST /login`
* `POST /reset-password`

### Endpoints protegidos

Requieren token de autenticación de **Laravel Sanctum** en el header:

```text
Authorization: Bearer <token>
```

Estos endpoints incluyen:

* `GET /me`
* `POST /logout`
* todos los endpoints de productos
* todos los endpoints de ventas
* todos los endpoints de recomendaciones
* todos los endpoints de reportes
* todos los endpoints de tiendas

---

# 1. Endpoints de autenticación

## POST /register

### Descripción

Registra un nuevo usuario en el sistema.

### Requiere autenticación

No

### Body esperado

```json
{
  "name": "Juan Perez",
  "email": "juan@example.com",
  "question": "Color favorito",
  "answer": "Azul",
  "password": "password123"
}
```

### Respuesta esperada

* Código `201 Created`
* Usuario registrado correctamente

---

## POST /login

### Descripción

Autentica un usuario y devuelve un token de acceso.

### Requiere autenticación

No

### Body esperado

```json
{
  "email": "juan@example.com",
  "password": "password123"
}
```

### Respuesta esperada

* Código `200 OK`
* Token de acceso
* Tipo de token
* Datos del usuario autenticado

---

## POST /reset-password

### Descripción

Restablece la contraseña de un usuario usando pregunta y respuesta de seguridad.

### Requiere autenticación

No

### Body esperado

```json
{
  "email": "juan@example.com",
  "question": "Color favorito",
  "answer": "Azul",
  "new_password": "password456"
}
```

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación

---

## GET /me

### Descripción

Obtiene la información del usuario autenticado.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Datos del usuario autenticado

---

## POST /logout

### Descripción

Cierra la sesión del usuario autenticado e invalida su token.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Mensaje de cierre de sesión exitoso

---

# 2. Endpoints de productos e inventario

## GET /products

### Descripción

Lista todos los productos registrados en el sistema.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Arreglo de productos

---

## POST /products

### Descripción

Crea un nuevo producto en el sistema.

### Requiere autenticación

Sí

### Body esperado

```json
{
  "name": "Teclado Redragon",
  "description": "Teclado mecánico",
  "price": 120.5,
  "stock": 8
}
```

### Respuesta esperada

* Código `201 Created`
* Mensaje de confirmación
* Producto creado

---

## GET /products/{id}

### Descripción

Obtiene la información de un producto específico.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador del producto

### Respuesta esperada

* Código `200 OK`
* Datos del producto

---

## PUT /products/{id}

### Descripción

Actualiza la información de un producto.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador del producto

### Body esperado

```json
{
  "name": "Teclado Redragon K552",
  "description": "Teclado mecánico actualizado",
  "price": 130,
  "stock": 6
}
```

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Producto actualizado

---

## DELETE /products/{id}

### Descripción

Elimina un producto del sistema.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador del producto

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación

---

## GET /products/{id}/stock

### Descripción

Consulta el stock disponible de un producto específico.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador del producto

### Respuesta esperada

* Código `200 OK`
* Identificador del producto
* Nombre del producto
* Stock actual

---

## PATCH /products/{id}/stock/decrease

### Descripción

Descuenta una cantidad específica del stock del producto.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador del producto

### Body esperado

```json
{
  "quantity": 2
}
```

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Stock anterior
* Cantidad descontada
* Stock actual

---

## PATCH /products/{id}/stock/increase

### Descripción

Aumenta una cantidad específica del stock del producto.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador del producto

### Body esperado

```json
{
  "quantity": 2
}
```

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Stock anterior
* Cantidad agregada
* Stock actual

---

# 3. Endpoints de ventas

## GET /sales

### Descripción

Lista todas las ventas registradas.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Arreglo de ventas

---

## GET /sales/{id}

### Descripción

Obtiene una venta específica por su identificador.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador de la venta

### Respuesta esperada

* Código `200 OK`
* Datos de la venta

---

## POST /sales

### Descripción

Registra una venta directamente desde el gateway hacia el microservicio de ventas.

### Requiere autenticación

Sí

### Body esperado

```json
{
  "userId": 1,
  "productId": 1,
  "productName": "Mouse Logitech G Pro",
  "quantity": 2,
  "unitPrice": 99.9
}
```

### Respuesta esperada

* Código `201 Created`
* Mensaje de confirmación
* Venta registrada

---

## GET /sales/user/{userId}

### Descripción

Consulta las ventas realizadas por un usuario específico.

### Requiere autenticación

Sí

### Parámetro de ruta

* `userId`: identificador del usuario

### Respuesta esperada

* Código `200 OK`
* Arreglo de ventas asociadas al usuario

---

## GET /sales/date-range/search

### Descripción

Consulta ventas registradas dentro de un rango de fechas.

### Requiere autenticación

Sí

### Parámetros de consulta

* `startDate`
* `endDate`

### Ejemplo

```text
/sales/date-range/search?startDate=2026-01-16&endDate=2026-06-16
```

### Respuesta esperada

* Código `200 OK`
* Arreglo de ventas dentro del rango

---

## POST /sales/process

### Descripción

Procesa una venta completa desde el gateway.

Este endpoint ejecuta el flujo principal del sistema:

* obtiene el usuario autenticado desde Sanctum
* consulta el producto en el microservicio de inventario
* valida stock disponible
* registra la venta en el microservicio de ventas
* descuenta el stock en el microservicio de inventario
* devuelve la respuesta final al cliente

### Requiere autenticación

Sí

### Body esperado

```json
{
  "productId": 1,
  "quantity": 2
}
```

### Respuesta esperada

* Código `201 Created`
* Mensaje de venta procesada correctamente
* Información de la venta registrada
* Información del stock actualizado

---

# 4. Endpoints de recomendaciones

## GET /recommendations/top-selling

### Descripción

Obtiene recomendaciones basadas en los productos más vendidos con stock disponible.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Arreglo de recomendaciones

---

## GET /recommendations/user

### Descripción

Obtiene recomendaciones personalizadas para el usuario autenticado a partir de su historial de compras y productos con stock.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Arreglo de recomendaciones

---

## GET /recommendations/price-max

### Descripción

Obtiene recomendaciones de productos más vendidos cuyo precio no supera el valor máximo enviado.

### Requiere autenticación

Sí

### Parámetro de consulta

* `maxPrice`: precio máximo permitido

### Ejemplo

```text
/recommendations/price-max?maxPrice=150
```

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Arreglo de recomendaciones

---

# 5. Endpoints de reportes

## GET /reports/total-sales

### Descripción

Genera un reporte general con el total de unidades vendidas y el total de ingresos.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Total de productos vendidos
* Total de ingresos

---

## GET /reports/sales-by-product

### Descripción

Genera un reporte agrupado por producto.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Arreglo con productos, cantidades vendidas y total de ingresos por producto

---

## GET /reports/sales-by-user

### Descripción

Genera un reporte agrupado por usuario.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Mensaje de confirmación
* Arreglo con usuarios, total de productos comprados y total gastado

---

# 6. Endpoints de tiendas y cobertura

## GET /stores

### Descripción

Lista todas las tiendas registradas.

### Requiere autenticación

Sí

### Respuesta esperada

* Código `200 OK`
* Arreglo de tiendas

---

## GET /stores/{id}

### Descripción

Obtiene la información de una tienda específica.

### Requiere autenticación

Sí

### Parámetro de ruta

* `id`: identificador de la tienda

### Respuesta esperada

* Código `200 OK`
* Datos de la tienda

---

## POST /stores

### Descripción

Registra una nueva tienda física en el sistema.

### Requiere autenticación

Sí

### Body esperado

```json
{
  "name": "Tienda Norte",
  "address": "Avenida 10 #20-30",
  "city": "Bogota",
  "latitude": 4.7001,
  "longitude": -74.0502,
  "productIds": [1, 3]
}
```

### Respuesta esperada

* Código `201 Created`
* Mensaje de confirmación
* Tienda creada

---

## GET /stores/city/{city}

### Descripción

Filtra las tiendas registradas por ciudad.

### Requiere autenticación

Sí

### Parámetro de ruta

* `city`: nombre de la ciudad

### Respuesta esperada

* Código `200 OK`
* Arreglo de tiendas de la ciudad indicada

---

## GET /stores/product/{productId}

### Descripción

Consulta las tiendas que tienen disponible un producto específico.

### Requiere autenticación

Sí

### Parámetro de ruta

* `productId`: identificador del producto

### Respuesta esperada

* Código `200 OK`
* Arreglo de tiendas que contienen ese producto en `productIds`

---

# Notas generales

* Todos los endpoints protegidos deben recibir un token válido de **Laravel Sanctum**.
* El cliente nunca consume directamente Flask, Express ni Django.
* El gateway es el único responsable de comunicarse con los microservicios internos.
* El endpoint `POST /sales/process` representa el flujo principal del sistema.
* Los endpoints de recomendaciones y reportes funcionan a partir de la información que el gateway recopila y envía a los microservicios correspondientes.
