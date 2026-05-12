# Microservices Commerce Platform (Release #2)

Sistema backend distribuido para una plataforma de comercio, desarrollado con arquitectura de microservicios. El sistema utiliza un API Gateway como único punto de entrada y se compone de servicios para autenticación, catálogo e inventario, ventas, recomendaciones, reportes y cobertura de tiendas.

## Autor

Alejandro Bermúdez Murcia

## Estructura del proyecto

```bash
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
├── README.md
└── .gitignore
```

---

## Documentación de microservicios

La documentación relacionada con la arquitectura, despliegue y funcionamiento de los microservicios se encuentra en:

- [Documentación de servicios](services/README-services.md)

---

## Pruebas unitarias

Las pruebas unitarias fueron implementadas en el microservicio `recommendations-django`.

Documentación:

- [Documentación de pruebas unitarias](services/recommendations-django/README-unit-tests.md)

---

## Pruebas de rendimiento

Las pruebas de rendimiento fueron desarrolladas utilizando Locust y se encuentran en la carpeta `testing`.

Documentación:

- [Documentación de pruebas de rendimiento](testing/README-testing.md)