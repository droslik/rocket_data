import django_filters
from .models import Entity


class EntityFilter(django_filters.FilterSet):
    country = django_filters.Filter(field_name='contact__address__country')
    city = django_filters.Filter(field_name='contact__address__city')
    product = django_filters.Filter(field_name='products__id')

    class Meta:
        model = Entity
        fields = [
            'country',
            'city',
            'product'
        ]
