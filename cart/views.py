from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartItemModelSerializer, AddToCartModelSerializer

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_items = CartItem.objects.filter(cart=cart)

        serializer = CartItemModelSerializer(cart_items, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = AddToCartModelSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        size = serializer.validated_data['size']
        quantity = serializer.validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity

            cart_item.save()

        return Response({"message": "Item added to cart"})
    
    def patch(self, request, pk):
        cart = request.user.cart
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        quantity = request.data.get("quantity")

        if quantity is None or int(quantity) <= 0:
            return Response({"error": "Invalid quantity"}, status=400)

        cart_item.quantity = quantity

        cart_item.save()

        return Response({"message": "Quantity updated"})
    
    def delete(self, request, pk):
        cart = request.user.cart
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        
        cart_item.delete()

        return Response({"message": "Item removed"})
