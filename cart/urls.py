from django.urls import path
from .views import AddToCart

urlpatterns = [
    path('', AddToCart.as_view(), name='add to cart'),
]