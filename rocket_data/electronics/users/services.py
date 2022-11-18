from users.models import User, UserAPIKey
from electronics.tasks import send_mail_api_key


def perform_create_user_and_api_key(self, validated_data):
    user = User.objects.create_user(**validated_data)
    if user:
        api_key, key = UserAPIKey.objects.create_key(
            user=user,
            name='electronics'
        )
        email = user.email
        send_mail_api_key.delay(email, key)
    return user
