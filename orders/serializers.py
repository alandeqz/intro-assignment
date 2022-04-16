from rest_framework import serializers 
from .models import Order
from users.models import User

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()
    user = serializers.IntegerField()
    is_active = serializers.BooleanField()

    class Meta:
        model = Order
        fields = (
            'id',
            'price',
            'user',
            'is_active'
        )
