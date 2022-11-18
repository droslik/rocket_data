from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from products.models import Product
from products.serializers import ProductSerializer


class ProductCRUDViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet):
    """Class to perform CRUD operations with Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
