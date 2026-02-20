from rest_framework import serializers
from .models import CartItem, Cart
from products.serializers import ProductModelSerializer

class CartItemModelSerializer(serializers.ModelSerializer):
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'size', 'quantity']

class CartModelSerializer(serializers.ModelSerializer):
    items = CartItemModelSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']

class AddToCartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'size', 'quantity']
