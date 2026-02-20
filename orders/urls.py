from django.urls import path
from .views import CreateOrderView, OrderListView

urlpatterns = [
    path('create-order/', CreateOrderView.as_view()),
    path('my-orders/', OrderListView.as_view()),
]
