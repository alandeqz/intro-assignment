from rest_framework import serializers

from orders.serializers import OrderSerializer 
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = (
            'id'
            'first_name',
            'last_name',
            'balance'
        )
