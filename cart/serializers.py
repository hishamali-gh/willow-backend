from rest_framework import serializers
from .models import CartItem, Cart
from products.serializers import ProductModelSerializer

class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id']
        read_only_fields = ['id']

class CartItemModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'size', 'quantity']

class AddToCartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'size', 'quantity']
