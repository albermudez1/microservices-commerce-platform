Flujo principal del sistema
Descripción general
El flujo principal del sistema es el procesamiento de una venta.
Este flujo se realiza a través del API Gateway, que actúa como único punto de entrada para el cliente y como orquestador entre los microservicios.
Flujo básico de venta
El usuario inicia sesión en el sistema a través del Laravel Gateway.
El usuario envía una solicitud para comprar un producto.
El gateway obtiene el usuario autenticado.
El gateway consulta el producto en el microservicio de catálogo e inventario.
El gateway valida que el producto exista.
El gateway valida que haya stock suficiente.
El gateway envía la información al microservicio de ventas para registrar la venta.
El microservicio de ventas guarda la venta en la base de datos.
El gateway solicita al microservicio de catálogo e inventario descontar el stock.
El gateway devuelve una respuesta final al cliente con la venta registrada y el stock actualizado.
Servicios involucrados
Laravel Gateway
Se encarga de:
autenticar al usuario
recibir la solicitud del cliente
consultar los microservicios necesarios
coordinar el flujo completo de venta
devolver la respuesta final
Catalog and Inventory Service
Se encarga de:
consultar el producto
validar el stock disponible
actualizar el stock después de la venta
Sales Service
Se encarga de:
registrar la venta
almacenar la información de la compra realizada
Flujo resumido
Cliente → Gateway → Catálogo/Inventario → Ventas → Catálogo/Inventario → Gateway → Cliente
Resultado del flujo
Al finalizar el proceso:
la venta queda registrada correctamente
el stock del producto queda actualizado
el cliente recibe una respuesta consolidada desde el gateway
Nota
Este es el flujo principal del sistema porque representa la operación más importante del negocio: la venta de un producto.