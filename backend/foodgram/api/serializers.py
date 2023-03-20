from users.models import User
from rest_framework import serializers
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(
            RegexValidator(r'^[\w.@+-]+$', message='Проверьте username!'),
        )
    )

    class Meta:
        """Класс мета для модели пользователй."""
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name', 'password'
        )
