# Pruebas de rendimiento

## Descripción general

Para el proyecto se plantearon pruebas de rendimiento utilizando **Locust**, enfocadas en el flujo principal del sistema: el procesamiento de una venta.

```text
El endpoint principal evaluado es:

POST /api/sales/process
Este endpoint fue elegido porque representa el flujo central del negocio y permite evaluar la interacción entre los microservicios principales del sistema:
•	API Gateway 
•	Catalog and Inventory Service 
•	Sales Service 

Estructura de la carpeta de testing
testing/
├── locustfile.py
└── README.md

Requisitos previos
Antes de ejecutar las pruebas, se debe tener:
•	el sistema completamente levantado 
•	MongoDB corriendo 
•	MySQL corriendo 
•	PostgreSQL corriendo 
•	todos los microservicios activos 
•	el API Gateway activo en http://127.0.0.1:8000 
Además, se debe contar previamente con:
•	un usuario registrado en el sistema 
•	un producto creado en el sistema 
•	stock suficiente para ese producto 

Datos de prueba sugeridos
Usuario de prueba
Se recomienda crear manualmente un usuario como este:
{
  "name": "Usuario Prueba",
  "email": "test@example.com",
  "question": "Color favorito",
  "answer": "Azul",
  "password": "password123"
}
Producto de prueba
Se recomienda crear manualmente un producto con stock alto, por ejemplo:
{
  "name": "Producto Prueba",
  "description": "Producto para pruebas de rendimiento",
  "price": 100,
  "stock": 10000
}
Se asume que este producto tendrá id = 1 para la prueba del archivo locustfile.py.

Instalación de Locust
Instalar Locust con:
pip install locust

Ejecución de la prueba
Ubicarse dentro de la carpeta testing y ejecutar:
locust -f locustfile.py --host=http://127.0.0.1:8000
Luego abrir en el navegador:
http://localhost:8089
Desde la interfaz web de Locust se pueden configurar los usuarios virtuales y la tasa de carga.

Escenarios propuestos
1. Prueba de carga
Objetivo: evaluar el comportamiento del sistema bajo una carga normal.
Configuración sugerida:
•	Usuarios: 10 
•	Spawn rate: 2 
•	Duración aproximada: 2 minutos 
2. Prueba de estrés
Objetivo: evaluar el comportamiento del sistema bajo una carga más alta.
Configuración sugerida:
•	Usuarios: 50 
•	Spawn rate: 5 
•	Duración aproximada: 2 minutos 
3. Prueba de pico
Objetivo: evaluar la respuesta del sistema ante un incremento repentino de usuarios.
Configuración sugerida:
•	Usuarios: 30 
•	Spawn rate: 30 
•	Duración aproximada: 1 minuto 

Flujo evaluado en la prueba
Cada usuario virtual ejecuta el siguiente flujo:
1.	inicia sesión en el sistema 
2.	obtiene el token de autenticación 
3.	consume el endpoint POST /api/sales/process 
4.	repite la operación mientras la prueba esté activa
