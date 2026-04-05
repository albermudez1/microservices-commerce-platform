from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def parse_positive_int(value):
    try:
        parsed = int(value)
        return parsed if parsed > 0 else None
    except (TypeError, ValueError):
        return None

@csrf_exempt
def health_check(request):
    return JsonResponse({
        "message": "Recommendations service is running."
    })


@csrf_exempt
def top_selling_recommendations(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Método no permitido."
        }, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido."
        }, status=400)

    sales = body.get('sales', [])
    products = body.get('products', [])

    if not isinstance(sales, list) or not isinstance(products, list):
        return JsonResponse({
            "error": "Los campos sales y products deben ser listas."
        }, status=400)

    sales_count = {}

    for sale in sales:
        product_id = parse_positive_int(sale.get('productId'))
        quantity = sale.get('quantity', 0)

        if product_id is None:
            continue

        if not isinstance(quantity, int) or quantity <= 0:
            continue

        if product_id not in sales_count:
            sales_count[product_id] = 0

        sales_count[product_id] += quantity

    available_products = []

    for product in products:
        product_id = parse_positive_int(product.get('id'))
        stock = product.get('stock', 0)

        if product_id is None:
            continue

        if not isinstance(stock, int) or stock <= 0:
            continue

        if product_id in sales_count:
            product_with_sales = product.copy()
            product_with_sales['totalSold'] = sales_count[product_id]
            available_products.append(product_with_sales)

    available_products.sort(key=lambda product: product['totalSold'], reverse=True)

    top_products = available_products[:5]

    return JsonResponse({
        "message": "Recomendaciones por productos más vendidos obtenidas correctamente.",
        "recommendations": top_products
    }, status=200)


@csrf_exempt
def user_recommendations(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Método no permitido."
        }, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido."
        }, status=400)

    user_id = body.get('userId')
    sales = body.get('sales', [])
    products = body.get('products', [])

    if user_id is None:
        return JsonResponse({
            "error": "El campo userId es requerido."
        }, status=400)

    if not isinstance(user_id, int) or user_id <= 0:
        return JsonResponse({
            "error": "El campo userId debe ser un entero positivo."
        }, status=400)

    if not isinstance(sales, list) or not isinstance(products, list):
        return JsonResponse({
            "error": "Los campos sales y products deben ser listas."
        }, status=400)

    purchased_product_ids = set()

    for sale in sales:
        sale_user_id = sale.get('userId')
        product_id = parse_positive_int(sale.get('productId'))

        if sale_user_id == user_id and product_id is not None:
            purchased_product_ids.add(product_id)

    recommended_products = []

    for product in products:
        product_id = parse_positive_int(product.get('id'))
        stock = product.get('stock', 0)

        if product_id is None:
            continue

        if not isinstance(stock, int) or stock <= 0:
            continue

        if product_id in purchased_product_ids:
            recommended_products.append(product)

    top_products = recommended_products[:5]

    return JsonResponse({
        "message": "Recomendaciones por historial de compra obtenidas correctamente.",
        "recommendations": top_products
    }, status=200)


@csrf_exempt
def price_max_recommendations(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Método no permitido."
        }, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido."
        }, status=400)

    max_price = body.get('maxPrice')
    sales = body.get('sales', [])
    products = body.get('products', [])

    if max_price is None:
        return JsonResponse({
            "error": "El campo maxPrice es requerido."
        }, status=400)

    if not isinstance(max_price, (int, float)) or max_price < 0:
        return JsonResponse({
            "error": "El campo maxPrice debe ser un número mayor o igual a 0."
        }, status=400)

    if not isinstance(sales, list) or not isinstance(products, list):
        return JsonResponse({
            "error": "Los campos sales y products deben ser listas."
        }, status=400)

    sales_count = {}

    for sale in sales:
        product_id = parse_positive_int(sale.get('productId'))
        quantity = sale.get('quantity', 0)

        if product_id is None:
            continue

        if not isinstance(quantity, int) or quantity <= 0:
            continue

        if product_id not in sales_count:
            sales_count[product_id] = 0

        sales_count[product_id] += quantity

    filtered_products = []

    for product in products:
        product_id = parse_positive_int(product.get('id'))
        stock = product.get('stock', 0)
        price = product.get('price')

        if product_id is None or price is None:
            continue

        if not isinstance(stock, int) or stock <= 0:
            continue

        if not isinstance(price, (int, float)) or price < 0:
            continue

        if product_id in sales_count and price <= max_price:
            product_with_sales = product.copy()
            product_with_sales['totalSold'] = sales_count[product_id]
            filtered_products.append(product_with_sales)

    filtered_products.sort(key=lambda product: product['totalSold'], reverse=True)

    top_products = filtered_products[:5]

    return JsonResponse({
        "message": "Recomendaciones por precio máximo obtenidas correctamente.",
        "recommendations": top_products
    }, status=200)




