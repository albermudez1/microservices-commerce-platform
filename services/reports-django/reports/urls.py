from django.urls import path
from .views import health_check, total_sales_report, sales_by_product_report, sales_by_user_report

urlpatterns = [
    path('health', health_check),
    path('total-sales', total_sales_report),
    path('sales-by-product', sales_by_product_report),
    path('sales-by-user', sales_by_user_report),
]
