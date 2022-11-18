from django.urls import path, include
from .views import ProductCRUDViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductCRUDViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
]
