from users.models import User, Subscription
from food.models import Tag, Recipe, Ingredient, Favorite, IngredientRecipe
from rest_framework import serializers
from django.core.validators import RegexValidator
import webcolors
from djoser.serializers import TokenCreateSerializer
from rest_framework.relations import StringRelatedField
from rest_framework.validators import UniqueTogetherValidator


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
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Класс мета для модели пользователй."""
        model = User
        fields = (
            'email', 'id', 'username', 'is_subscribed',
            'first_name', 'last_name', 'password'
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop("password", None)
        return response

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user_id = request.user.id
        return Subscription.objects.filter(
            user_id=user_id, subscriber_id=obj.id
        ).exists()


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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для игридиента."""
    name = StringRelatedField(source='ingredient.name')
    measurement_unit = StringRelatedField(source='ingredient.measurement_unit')

    class Meta:
        """Класс мета для модели ингридиент."""
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецепта."""
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(source='recipe', many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Класс мета для модели рецепта."""
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'name', 'image',
                  'text', 'cooking_time'
                  )

    def get_is_favorited(self, obj):
        request = self.context['request']
        user_id = request.user.id
        return Favorite.objects.filter(
            user_id=user_id, recipe_id=obj.id
        ).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    email = StringRelatedField(source='subscriber.email')
    id = serializers.IntegerField(source='subscriber.id', read_only=True)
    username = StringRelatedField(source='subscriber.username')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    subscriber = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    first_name = StringRelatedField(source='subscriber.first_name')
    last_name = StringRelatedField(source='subscriber.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """Класс мета для модели рецепта."""
        model = Subscription
        fields = ('email', 'user', 'subscriber', 'id', 'username',
                  'is_subscribed', 'first_name', 'last_name',
                  'recipes', 'recipes_count'
                  )

        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscriber')
            ),
        )

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user_id=obj.user.id, subscriber_id=obj.subscriber.id
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.subscriber)
        return RecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        count = len(Recipe.objects.filter(author=obj.subscriber))
        return count


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='favorites.id', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe = RecipeSerializer(default="auto_replace_me")
    name = StringRelatedField(source='favorites.name', read_only=True)
    cooking_time = serializers.IntegerField(
        source='favorites.cooking_time',
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe', 'name', 'cooking_time')

        validators = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            ),
        )
