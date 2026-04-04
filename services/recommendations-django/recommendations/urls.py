from django.urls import path
from .views import (
    health_check,
    top_selling_recommendations,
    user_recommendations,
    price_max_recommendations,
)

urlpatterns = [
    path('health', health_check),
    path('top-selling', top_selling_recommendations),
    path('user', user_recommendations),
    path('price-max', price_max_recommendations),
]
