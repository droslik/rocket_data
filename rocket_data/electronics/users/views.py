from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializers import UserCreateSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """Class for registrations of users. Allowed for any user"""
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )


