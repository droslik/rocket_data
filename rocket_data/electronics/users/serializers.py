from rest_framework import serializers
from .models import User
from entities.models import Entity
from .services import perform_create_user_and_api_key


class UserCreateSerializer(serializers.ModelSerializer):
    """User Serializer for registration"""
    entity = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Entity.objects.all()
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'entity',
            'entity_id',
        ]

    def create(self, validated_data):
        return perform_create_user_and_api_key(self, validated_data)

