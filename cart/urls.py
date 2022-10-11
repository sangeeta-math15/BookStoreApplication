from django.urls import path
from .views import AddToCart, CheckOut

urlpatterns = [
    path('', AddToCart.as_view(), name='add to cart'),
    path('checkout', CheckOut.as_view(), name='CheckOut'),
]