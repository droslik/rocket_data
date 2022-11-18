from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from .filters import EntityFilter
from .models import Entity
from .serializers import (
    EntityCreateSerializer,
    FactoryCreateSerializer,
    EntityDetailSerializer,
    EntityListSerializer
)
from .services import retrieve_entity, retrieve_entity_supplier, get_statistics


class FactoryListCreateAPIView(mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               GenericViewSet):
    """Class to perform CRUD operations with factories for admin"""
    queryset = Entity.objects.all()
    serializer_class = FactoryCreateSerializer
    permission_classes = (IsAdminUser, )


class EntityListCreateAPIView(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    """Class to perform CRUD operations with other entities for admin"""
    queryset = Entity.objects.all()
    serializer_class = EntityCreateSerializer
    permission_classes = (IsAdminUser,)


class EntityDetailAPIView(generics.RetrieveAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntityDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        return retrieve_entity_supplier(self, request, *args, **kwargs)


class EntityListViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    """Class to view all entities with filters and statistics"""
    queryset = Entity.objects.all()
    serializer_class = EntityListSerializer
    permission_classes = (IsAdminUser, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = EntityFilter

    @action(methods=['GET'], detail=False, url_path='statistics')
    def statistics(self, request, *args, **kwargs):
        return get_statistics(self, request, *args, **kwargs)


class EntityDetailViewSet(mixins.RetrieveModelMixin,
                          GenericViewSet):
    """Class to view own company"""
    queryset = Entity.objects.all()
    serializer_class = EntityListSerializer

    def retrieve(self, request, pk=None):
        return retrieve_entity(self, request, pk)
