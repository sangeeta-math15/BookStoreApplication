from django.db import models
from user.models import User


class Book(models.Model):
    author = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    price = models.IntegerField()
    quantity = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
