from django.urls import path, include
from .views import (
    EntityListCreateAPIView,
    FactoryListCreateAPIView,
    EntityDetailAPIView,
    EntityListViewSet,
    EntityDetailViewSet,
    )
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'all', EntityListViewSet, basename='entities-all')
router.register(r'factories', FactoryListCreateAPIView, basename='factories')
router.register(r'others', EntityListCreateAPIView, basename='others')
router.register(r'detail', EntityDetailViewSet, basename='detail')

urlpatterns = [
   path('entities/<int:pk>/', EntityDetailAPIView.as_view(), name='entity-detail'),
   path('entities/', include(router.urls)),
]
