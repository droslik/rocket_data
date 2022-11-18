from django.urls import path
from .views import UserRegistrationAPIView


urlpatterns = [
    path(
        'users/create/',
        UserRegistrationAPIView.as_view(),
        name='users-create'
    )
]
