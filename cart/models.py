from book.models import Book
from user.models import User
from django.db import models


class Cart(models.Model):
    total_quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)
    status = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()