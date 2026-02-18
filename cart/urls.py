from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartAPIView.as_view()),
    path('cart/<int:pk>/', views.CartAPIView.as_view()),
]
