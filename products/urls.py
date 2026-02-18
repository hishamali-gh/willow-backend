from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('product-types', views.ProductTypeModelViewSet, basename='product-types')
router.register('products', views.ProductModelViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls))
]
