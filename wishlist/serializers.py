from rest_framework import serializers
from products.serializers import ProductModelSerializer
from .models import Wishlist
from products.models import Product

class WishlistModelSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    product_details = ProductModelSerializer(
        source='product',
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_details', 'created_at']
        read_only_fields = ['id', 'created_at']

