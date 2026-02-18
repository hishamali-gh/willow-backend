from rest_framework import serializers
from .models import ProductType, Product

class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'product_type',
            'description',
            'price',
            'count',
            'created_at',
            'updated_at'
        ]
