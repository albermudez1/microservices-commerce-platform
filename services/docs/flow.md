# Flujo principal del sistema

## Descripción general

El flujo principal del sistema corresponde al procesamiento de una venta.  
Este flujo se ejecuta a través del **API Gateway**, que funciona como único punto de entrada para el cliente y como orquestador entre los microservicios principales del sistema.

## Flujo principal de venta

1. El usuario inicia sesión en el sistema a través del **Laravel Gateway**.
2. El usuario envía una solicitud para comprar un producto.
3. El **gateway** obtiene el usuario autenticado.
4. El **gateway** consulta el producto en el microservicio de **catálogo e inventario**.
5. El **gateway** valida que el producto exista.
6. El **gateway** valida que haya stock suficiente.
7. El **gateway** envía la información al microservicio de **ventas** para registrar la venta.
8. El microservicio de **ventas** guarda la venta en la base de datos.
9. El **gateway** solicita al microservicio de **catálogo e inventario** descontar el stock.
10. El **gateway** devuelve una respuesta final al cliente con la venta registrada y el stock actualizado.

## Servicios involucrados en el flujo principal

### Laravel Gateway
Se encarga de:
- autenticar al usuario
- recibir la solicitud del cliente
- consultar los microservicios necesarios
- coordinar el flujo completo de venta
- devolver la respuesta final

### Catalog and Inventory Service
Se encarga de:
- consultar el producto
- validar el stock disponible
- actualizar el stock después de la venta

### Sales Service
Se encarga de:
- registrar la venta
- almacenar la información de la compra realizada

## Flujo resumido

**Cliente → Gateway → Catálogo/Inventario → Ventas → Catálogo/Inventario → Gateway → Cliente**

## Resultado del flujo principal

Al finalizar el proceso:

- la venta queda registrada correctamente
- el stock del producto queda actualizado
- el cliente recibe una respuesta consolidada desde el gateway

---

# Flujos complementarios del sistema

Además del flujo principal de venta, el sistema cuenta con otros flujos complementarios que también se ejecutan a través del **API Gateway**.

## 1. Flujo de recomendaciones

Este flujo permite generar recomendaciones de productos para el usuario.

### Recomendaciones por productos más vendidos
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta los productos en **catálogo e inventario**.
3. El **gateway** consulta las ventas registradas en el microservicio de **ventas**.
4. El **gateway** envía esa información al microservicio de **recomendaciones**.
5. El microservicio de **recomendaciones** procesa la lógica correspondiente.
6. El **gateway** devuelve la respuesta final al cliente.

### Recomendaciones por historial de usuario
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** obtiene el usuario autenticado.
3. El **gateway** consulta productos y ventas.
4. El **gateway** envía la información al microservicio de **recomendaciones**.
5. El microservicio procesa las compras previas del usuario.
6. El **gateway** devuelve la respuesta con las recomendaciones.

### Recomendaciones por precio máximo
1. El cliente realiza la solicitud al **gateway** indicando un precio máximo.
2. El **gateway** consulta productos y ventas.
3. El **gateway** envía esa información al microservicio de **recomendaciones**.
4. El microservicio filtra los productos según el precio máximo y la lógica definida.
5. El **gateway** devuelve la respuesta final al cliente.

## 2. Flujo de reportes

Este flujo permite generar reportes a partir de las ventas registradas.

### Reporte de ventas totales
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta todas las ventas en el microservicio de **ventas**.
3. El **gateway** envía la información al microservicio de **reportes**.
4. El microservicio genera el reporte.
5. El **gateway** devuelve la respuesta final al cliente.

### Reporte de ventas por producto
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta las ventas registradas.
3. El **gateway** envía la información al microservicio de **reportes**.
4. El microservicio agrupa la información por producto.
5. El **gateway** devuelve la respuesta final al cliente.

### Reporte de ventas por usuario
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta las ventas registradas.
3. El **gateway** envía la información al microservicio de **reportes**.
4. El microservicio agrupa la información por usuario.
5. El **gateway** devuelve la respuesta final al cliente.

## 3. Flujo de cobertura de tiendas

Este flujo permite consultar información de tiendas físicas registradas en el sistema.

### Consulta general de tiendas
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta el microservicio de **cobertura de tiendas**.
3. El microservicio devuelve la lista de tiendas registradas.
4. El **gateway** devuelve la respuesta final al cliente.

### Consulta de tienda por identificador
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta el microservicio de **cobertura de tiendas** con el id solicitado.
3. El microservicio devuelve la información de la tienda.
4. El **gateway** devuelve la respuesta final al cliente.

### Consulta de tiendas por ciudad
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta el microservicio de **cobertura de tiendas** filtrando por ciudad.
3. El microservicio devuelve las tiendas encontradas.
4. El **gateway** devuelve la respuesta final al cliente.

### Consulta de tiendas por producto
1. El cliente realiza la solicitud al **gateway**.
2. El **gateway** consulta el microservicio de **cobertura de tiendas** filtrando por producto.
3. El microservicio devuelve las tiendas asociadas a ese producto.
4. El **gateway** devuelve la respuesta final al cliente.

## Resumen final

El sistema cuenta con:

- un **flujo principal**, correspondiente a la venta de un producto
- varios **flujos complementarios**, como recomendaciones, reportes y cobertura de tiendas

Todos estos flujos siguen la misma regla arquitectónica:

**Cliente → Gateway → Microservicio correspondiente → Gateway → Cliente**