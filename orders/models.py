from django.db import models

from users.models import User

# Create your models here.

class Order(models.Model):
    id=models.IntegerField(primary_key=True)
    price=models.IntegerField()
    user=models.IntegerField()
    is_active=models.BooleanField()
