from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework.response import Response
from electronics.tasks import send_email_qr
from entities.models import Address, Contact, Entity
from users.models import User, UserAPIKey


def perform_create_factory(self, validated_data):
    contact_data = validated_data.pop('contact')
    email_data = contact_data.pop('email')
    address_data = contact_data.pop('address')
    products = validated_data['products']
    address = Address.objects.create(**address_data)
    contact = Contact.objects.create(email=email_data, address_id=address.id)
    entity = Entity.objects.create(
        name=validated_data['name'],
        type=validated_data['type'],
        contact_id=address.id,
        )
    for product in products:
        entity.products.add(product)
    return entity


def perform_update_factory(self, instance, validated_data):
    if validated_data:
        contact_data = validated_data.pop('contact')
        address_data = contact_data.pop('address')
        products = validated_data['products']
        instance.name = validated_data.get('name', instance.name)
        instance.contact.email = contact_data.get(
            'email', instance.contact.email
        )
        instance.contact.address.country = address_data.get(
            'country', instance.contact.address.country
        )
        instance.contact.address.city = address_data.get(
            'city', instance.contact.address.city
        )
        instance.contact.address.street = address_data.get(
            'street', instance.contact.address.street
        )
        instance.contact.address.building = address_data.get(
            'building', instance.contact.address.building
        )
        for product in products:
            instance.products.add(product)
        instance.save()
        return instance


def perform_create_entity(self, validated_data):
    contact_data = validated_data.pop('contact')
    email_data = contact_data.pop('email')
    address_data = contact_data.pop('address')
    products = validated_data['products']
    supplier = validated_data.pop('supplier')
    entity_level = validated_data.get('type').level
    supplier_level = supplier.type.level
    if entity_level <= supplier_level:
        raise serializers.ValidationError(
            'The type level of Supplier should be lower than Entity type level'
        )
    address = Address.objects.create(**address_data)
    contact = Contact.objects.create(email=email_data, address_id=address.id)
    entity = Entity.objects.create(
        name=validated_data['name'],
        type=validated_data['type'],
        contact_id=address.id,
        supplier=supplier
    )
    for product in products:
        entity.products.add(product)
    return entity


def perform_update_entity(self, instance, validated_data):
    if validated_data:
        contact_data = validated_data.pop('contact')
        address_data = contact_data.pop('address') #
        products = validated_data['products']
        instance.supplier = validated_data.get('supplier', instance.supplier)
        supplier = validated_data.pop('supplier')
        entity_level = validated_data.get('type').level
        supplier_level = supplier.type.level
        if entity_level <= supplier_level:
            raise serializers.ValidationError(
                'The type level of Supplier should be lower than Entity type level'
            )
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.contact.email = contact_data.get(
            'email', instance.contact.email
        )
        instance.contact.address.country = address_data.get(
            'country', instance.contact.address.country
        )
        instance.contact.address.city = address_data.get(
            'city', instance.contact.address.city
        )
        instance.contact.address.street = address_data.get(
            'street', instance.contact.address.street
        )
        instance.contact.address.building = address_data.get(
            'building', instance.contact.address.building
        )
        for product in products:
            instance.products.add(product)
        instance.save()
        return instance


def retrieve_entity_supplier(self, request, *args, **kwargs):
    user = request.user
    if not user.is_superuser:
        user = get_user(request)
        if not user:
            return Response({'Can not authenticate user'})
        if not user.is_active:
            return Response({'You are not active user'})
        entity = user.entity
        supplier = entity.supplier
        supplier_data = self.serializer_class(
            supplier,
            context={'request': request}
        ).data
        return Response({'entity_details': supplier_data})
    pk = self.kwargs['pk']
    entity = Entity.objects.filter(pk=pk)
    if not entity:
        return Response({'message': 'Entity not found'})
    entity_data = self.serializer_class(
        entity[0],
        context={'request': request}
    ).data
    return Response({'entity': entity_data})


def retrieve_entity(self, request, pk):
    """Retrieve entity details which user belongs to"""
    user = request.user
    if not user.is_superuser:
        user = get_user(request)
        if not user:
            return Response({'Can not authenticate user'})
        if not user.is_active:
            return Response({'You are not active user'})
        entity = user.entity
        if not entity:
            return Response({'Not found'})
        data = entity.contact.address
        new_data = {'country': data.country,
                    'city': data.city,
                    'street': data.street,
                    'building': data.building}
        entity_name = entity.name
        email = user.email
        send_email_qr.delay(email, new_data, entity_name)
        entity_data = self.serializer_class(
            entity,
            context={'request': request}
        ).data
        return Response({'entity_details': entity_data})
    entity = Entity.objects.filter(pk=pk)
    if not entity:
        return Response({'message': 'Entity not found'})
    data = entity[0].contact.address
    new_data = {'country': data.country,
                'city': data.city,
                'street': data.street,
                'building': data.building}
    entity_name = entity[0].name
    email = user.email
    send_email_qr.delay(email, new_data, entity_name)
    entity_data = self.serializer_class(
        entity[0],
        context={'request': request}
    ).data
    return Response({'entity': entity_data})


def get_user(request):
    """Retrieve a user based on the request API key."""
    key = request.META["HTTP_AUTHORIZATION"].split()[1]
    try:
        api_key = UserAPIKey.objects.get_from_key(key)
    except UserAPIKey.DoesNotExist:
        raise serializers.ValidationError({'message': 'Invalid Api Key'})
    user = User.objects.get(api_keys=api_key)
    return user


def get_statistics(self, request, *args, **kwargs):
    entities_debt_greater_avg = Entity.objects.filter(
        debt__gt=(Entity.objects.aggregate(
            avg_debt=Round(Avg('debt'), 2)))['avg_debt'])
    serializer = self.serializer_class(
        data=entities_debt_greater_avg,
        context={'request': request},
        many=True
    )
    serializer.is_valid()
    return Response(
        {'entities with debt higher than average': serializer.data}
    )
