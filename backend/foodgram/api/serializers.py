from users.models import User
from food.models import Tag, Recipe, Ingredient
from rest_framework import serializers
from django.core.validators import RegexValidator
import webcolors
from djoser.serializers import TokenCreateSerializer


class Hex2NameColor(serializers.Field):
    """Поле сериализатор для цвета."""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


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
            'email', 'id', 'username',
            'first_name', 'last_name', 'password'
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop("password", None)
        return response


class GetTokenSerializer(TokenCreateSerializer):
    """Сериализатор для получения токена."""
    class Meta:
        """Класс мета для токена."""
        model = User
        fields = ('email', 'password')


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о текущем пользователе."""
    class Meta:
        """Класс мета для модели пользователй."""
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
        )


class PasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пароля."""
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        """Класс мета для изменения пароля."""
        model = User
        fields = ('new_password', 'current_password')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тега."""
    color = Hex2NameColor()

    class Meta:
        """Класс мета для модели тег."""
        model = Tag
        fields = ('id', 'name',
                  'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для игридиента."""
    class Meta:
        """Класс мета для модели ингридиент."""
        model = Ingredient
        fields = ('id', 'name',
                  'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецепта."""
    class Meta:
        """Класс мета для модели рецепта."""
        model = Recipe
        fields = ('id',)
