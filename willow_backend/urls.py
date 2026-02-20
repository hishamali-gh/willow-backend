from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acc/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls'))
]
