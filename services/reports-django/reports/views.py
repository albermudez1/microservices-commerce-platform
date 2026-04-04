from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def health_check(request):
    return JsonResponse({
        "message": "Reports service is running."
    })

@csrf_exempt
def total_sales_report(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Método no permitido."
        }, status=405)

    try:
        import json
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido."
        }, status=400)

    sales = body.get('sales', [])

    if not isinstance(sales, list):
        return JsonResponse({
            "error": "El campo sales debe ser una lista."
        }, status=400)

    total_revenue = 0
    total_items = 0

    for sale in sales:
        quantity = sale.get('quantity', 0)
        price = sale.get('price', 0)

        if not isinstance(quantity, int) or quantity <= 0:
            continue

        if not isinstance(price, (int, float)) or price < 0:
            continue

        total_items += quantity
        total_revenue += quantity * price

    return JsonResponse({
        "message": "Reporte de ventas totales generado correctamente.",
        "totalItemsSold": total_items,
        "totalRevenue": total_revenue
    }, status=200)

@csrf_exempt
def sales_by_product_report(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Método no permitido."
        }, status=405)

    try:
        import json
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido."
        }, status=400)

    sales = body.get('sales', [])

    if not isinstance(sales, list):
        return JsonResponse({
            "error": "El campo sales debe ser una lista."
        }, status=400)

    product_summary = {}

    for sale in sales:
        product_id = sale.get('productId')
        quantity = sale.get('quantity', 0)
        price = sale.get('price', 0)

        if product_id is None:
            continue

        if not isinstance(quantity, int) or quantity <= 0:
            continue

        if not isinstance(price, (int, float)) or price < 0:
            continue

        if product_id not in product_summary:
            product_summary[product_id] = {
                "productId": product_id,
                "totalItemsSold": 0,
                "totalRevenue": 0
            }

        product_summary[product_id]["totalItemsSold"] += quantity
        product_summary[product_id]["totalRevenue"] += quantity * price

    result = list(product_summary.values())

    return JsonResponse({
        "message": "Reporte de ventas por producto generado correctamente.",
        "report": result
    }, status=200)

@csrf_exempt
def sales_by_user_report(request):
    if request.method != 'POST':
        return JsonResponse({
            "error": "Método no permitido."
        }, status=405)

    try:
        import json
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "JSON inválido."
        }, status=400)

    sales = body.get('sales', [])

    if not isinstance(sales, list):
        return JsonResponse({
            "error": "El campo sales debe ser una lista."
        }, status=400)

    user_summary = {}

    for sale in sales:
        user_id = sale.get('userId')
        quantity = sale.get('quantity', 0)
        price = sale.get('price', 0)

        if user_id is None:
            continue

        if not isinstance(quantity, int) or quantity <= 0:
            continue

        if not isinstance(price, (int, float)) or price < 0:
            continue

        if user_id not in user_summary:
            user_summary[user_id] = {
                "userId": user_id,
                "totalItemsPurchased": 0,
                "totalSpent": 0
            }

        user_summary[user_id]["totalItemsPurchased"] += quantity
        user_summary[user_id]["totalSpent"] += quantity * price

    result = list(user_summary.values())

    return JsonResponse({
        "message": "Reporte de ventas por usuario generado correctamente.",
        "report": result
    }, status=200)
