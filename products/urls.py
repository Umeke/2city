from django.contrib import admin
from django.urls import path
from products.views import ProductListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products', ProductListAPIView.as_view(), name='product-list'),
]
