from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Class to perform actions with products"""
    class Meta:
        model = Product
        fields = [
            'name',
            'model',
            'launch_date'
        ]
