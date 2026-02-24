from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import ProductType, Product, ProductVariant
from .serializers import ProductTypeModelSerializer, ProductModelSerializer, ProductVariantModelSerializer

class ProductTypeModelViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeModelSerializer
    permission_classes = [IsAdminUser]

class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'product_type', 'is_active']
    search_fields = ['name', 'description', 'category', 'product_type__name']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images').order_by('-created_at')

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        
        return [IsAdminUser()]
    
class ProductVariantAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            product_variant = get_object_or_404(ProductVariant, pk=pk)
            serializer = ProductVariantModelSerializer(product_variant)

            return Response(serializer.data, status=status.HTTP_200_OK)

        product_variants = ProductVariant.objects.all()
        serializer = ProductVariantModelSerializer(product_variants, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductVariantModelSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        product_variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = ProductVariantModelSerializer(product_variant, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        product_variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = ProductVariantModelSerializer(product_variant, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        product_variant = get_object_or_404(ProductVariant, pk=pk)

        product_variant.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
