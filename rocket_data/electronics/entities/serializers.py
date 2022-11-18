from rest_framework import serializers
from products.models import Product
from .models import Contact, Entity, Address, EntityType
from .services import (
    perform_create_factory,
    perform_create_entity,
    perform_update_entity,
    perform_update_factory
)


class AddressSerializer(serializers.ModelSerializer):
    """Address Serializer"""
    class Meta:
        model = Address
        fields = [
            'country',
            'city',
            'street',
            'building'
        ]


class ContactSerializer(serializers.ModelSerializer):
    """Contact Serializer includes Address"""
    address = AddressSerializer()

    class Meta:
        model = Contact
        fields = [
            'email',
            'address'
        ]


class FactoryCreateSerializer(serializers.ModelSerializer):
    """Class creates only Factory"""
    contact = ContactSerializer()
    type = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=EntityType.objects.filter(name='factory')
    )
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Entity
        fields = [
            'name',
            'type',
            'contact',
            'products',
            'created_at'
        ]

    def create(self, validated_data):
        return perform_create_factory(self, validated_data)

    def update(self, instance, validated_data):
        return perform_update_factory(self, instance, validated_data)


class EntityCreateSerializer(serializers.ModelSerializer):
    """Class creates Entities except for Factory"""
    contact = ContactSerializer()
    supplier = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Entity.objects.exclude(name='entrepreneur')
    )
    type = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=EntityType.objects.exclude(name='factory')
    )
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Entity
        fields = [
            'name',
            'type',
            'contact',
            'supplier',
            'products',
            'created_at'
        ]

    def create(self, validated_data):
        return perform_create_entity(self, validated_data)

    def update(self, instance, validated_data):
        return perform_update_entity(self, instance, validated_data)


class SupplierSerializer(serializers.Serializer):
    """Supplier serializer for adding link to the supplier"""
    pk = serializers.PrimaryKeyRelatedField(queryset=Entity.objects.filter())
    url = serializers.HyperlinkedIdentityField(
        view_name='entity-detail',
        lookup_field='pk',
    )


class EntityDetailSerializer(serializers.ModelSerializer):
    """Class to view basic details of Entity by pk
    Also is used for making link of supplier"""
    contact = ContactSerializer()

    class Meta:
        model = Entity
        fields = [
            'name',
            'type',
            'contact',
           ]


class EntityListSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = Entity
        fields = [
            'name',
            'type',
            'contact',
            'supplier',
            'products',
            'debt',
            'created_at'
        ]




