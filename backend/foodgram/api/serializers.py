import webcolors
import base64

from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.validators import UniqueValidator
from django.core.files.base import ContentFile


from food.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                         ShoppingCart, Tag, TagRecipe)
from users.models import Subscription, User
from django.db.models import Sum


class Base64ImageField(serializers.ImageField):
    """Класс раскодировки изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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


class MyUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(
            RegexValidator(r'^[\w.@+-]+$', message='Проверьте username!'),
            UniqueValidator(queryset=User.objects.all()),
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
        response = super(MyUserSerializer, self).to_representation(instance)
        response.pop("password", None)
        return response

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user_id = request.user.id
        return Subscription.objects.filter(
            user_id=user_id, subscriber_id=obj.id
        ).exists()


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
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для игредиента."""
    class Meta:
        """Класс мета для модели ингридиент."""
        model = Ingredient
        fields = ('id', 'name',
                  'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для игредиента рецепта."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        """Класс мета для модели ингредиент рецепт."""
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецепта."""
    tags = TagSerializer(many=True)
    author = MyUserSerializer(read_only=True, )
    ingredients = IngredientRecipeSerializer(source='recipe', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        """Класс мета для модели рецепта."""
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time'
                  )

    def get_is_favorited(self, obj):
        request = self.context['request']
        user_id = request.user.id
        return Favorite.objects.filter(
            user_id=user_id, recipe_id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        user_id = request.user.id
        return ShoppingCart.objects.filter(
            user_id=user_id, recipe_id=obj.id
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения рецепта."""
    author = MyUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(
        many=True
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        """Класс мета для модели рецепта."""
        model = Recipe
        fields = ('id', 'name', 'author',
                  'tags', 'ingredients',
                  'image',
                  'text', 'cooking_time'
                  )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            TagRecipe.objects.create(
                tag=tag,
                recipe=recipe,
            )
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredient').get('id')
            current_ingredient, status = Ingredient.objects.get_or_create(
                pk=ingredient_id)
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient.get('amount'))
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(id=instance.id).update(**validated_data)
        for tag in instance.tags.all():
            if tag in tags:
                tags.remove(tag)
                continue
            TagRecipe.objects.filter(recipe=instance, tag=tag).delete()
        for tag in tags:
            TagRecipe.objects.create(
                tag=tag,
                recipe=instance,
            )
        for ingredient in instance.ingredients.all():
            IngredientRecipe.objects.filter(
                recipe=instance,
                ingredient=ingredient
            ).delete()
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                pk=ingredient.get('ingredient').get('id'))
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient.get('amount'))
        instance = Recipe.objects.filter(id=instance.id).get()
        return instance

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(
            Tag.objects.filter(id__in=instance.tags.all()),
            many=True
        ).data
        representation['ingredients'] = IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=instance),
            many=True
        ).data
        return representation


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    email = StringRelatedField(source='subscriber.email')
    id = serializers.IntegerField(source='subscriber.id', read_only=True)
    username = StringRelatedField(source='subscriber.username')
    first_name = StringRelatedField(source='subscriber.first_name')
    last_name = StringRelatedField(source='subscriber.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        """Класс мета для модели рецепта."""
        model = Subscription
        fields = ('email', 'id', 'username',
                  'is_subscribed', 'first_name', 'last_name',
                  'recipes', 'recipes_count'
                  )

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user_id=obj.user.id, subscriber_id=obj.subscriber.id
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.subscriber)
        return RecipeSerializer(
            queryset,
            many=True,
            context={'request': self.context.get('request')}
        ).data

    def get_recipes_count(self, obj):
        count = len(Recipe.objects.filter(author=obj.subscriber))
        return count

    def validate(self, data):
        """Проверка на повтор."""
        subscription_id = self.context.get('subscription_id')
        user_id = self.context.get('request').user.id
        user = get_object_or_404(User, id=user_id)
        subscription = get_object_or_404(User, id=subscription_id)
        if user == subscription:
            raise serializers.ValidationError({
                'subscriber': 'Нельзя на себя'
            })
        if Subscription.objects.filter(
            user=user, subscriber=subscription
        ).exists():
            raise serializers.ValidationError({
                'subscriber': 'Данная пользователь уже в подписках'
            })
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""
    id = serializers.IntegerField(source='favorites.id', read_only=True)
    name = StringRelatedField(source='favorites.name', read_only=True)
    cooking_time = serializers.IntegerField(
        source='favorites.cooking_time',
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'cooking_time')

    def validate(self, data):
        """Проверка на повтор."""
        recipe_id = self.context.get('recipe_id')
        user_id = self.context.get('request').user.id
        if Favorite.objects.filter(
            user=user_id, recipe=recipe_id
        ).exists():
            raise serializers.ValidationError({
                'recipe': 'Данная рецепт уже в избраном'
            })
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""
    id = serializers.IntegerField(source='recipe.id', read_only=True)
    name = StringRelatedField(source='recipe.name', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'cooking_time')

    def validate(self, data):
        """Проверка на повтор."""
        recipe_id = self.context.get('recipe_id')
        user_id = self.context.get('request').user.id
        if ShoppingCart.objects.filter(
            user=user_id, recipe=recipe_id
        ).exists():
            raise serializers.ValidationError({
                'recipe': 'Данная рецепт уже в списке покупок'
            })
        return data


class GetShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""
    class Meta:
        model = ShoppingCart

    def to_representation(self, instance):
        response = {}
        query = IngredientRecipe.objects \
            .filter(recipe__in=instance.values('recipe')) \
            .values('ingredient').annotate(score=Sum('amount'))
        response['ingrideint'] = [
            {
                "name": Ingredient.objects.get(id=item.get('ingredient')).name,
                "measurement_unit":
                Ingredient.objects
                .get(id=item.get('ingredient'))
                .measurement_unit,
                "sum": item.get('score'),
            } for item in query]
        return response
