from rest_framework import filters, status, viewsets
from api.mixins import (
    CreateListRetrieveViewSet, ListRetrieveViewSet,
    CreateDestroyViewSet,
)
from users.models import User, Subscription
from food.models import Tag, Ingredient, Favorite, Recipe
from api.serializers import (
    UserSerializer, GetTokenSerializer,
    MeSerializer, PasswordSerializer,
    TagSerializer, IngredientSerializer,
    SubscriptionSerializer, FavoriteSerializer,
    RecipeSerializer,
)
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from djoser.views import TokenCreateView
from api.permissions import IsReadOnly


class UserViewSet(CreateListRetrieveViewSet):
    """Вьюсет для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(ListRetrieveViewSet):
    """Вьюсет для пользователей."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    """Вьюсет для пользователей."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


@api_view(['GET'])
def get_subscription(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        serializer = SubscriptionSerializer(user.follower.all(), many=True)
        print(user.follower.all())
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Вы не авторизованы',
        status=status.HTTP_401_UNAUTHORIZED
    )


class SubscribeViewSet(CreateDestroyViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsReadOnly,)

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            subscriber=self.get_user()
        )

    def delete(self, request, user_id):
        """Отписаться от автора."""
        subscription = get_object_or_404(
            Subscription,
            user=request.user,
            subscriber=get_object_or_404(User, id=user_id),
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsReadOnly,)

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    def get_queryset(self):
        return self.request.user.favorites.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe()
        )

    def delete(self, request, recipe_id):
        """Отписаться от автора."""
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id),
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomGetView(TokenCreateView):
    serializer_class = GetTokenSerializer


@api_view(['POST'])
def get_token(request):
    """Получение токена."""
    serializer = GetTokenSerializer(data=request.data)
    email = request.data.get('email')
    password = request.data.get('password')
    if serializer.is_valid():
        user = get_object_or_404(
            User, password=password, email=email
        )
        token = AccessToken.for_user(user)
        return Response(
            {'auth_token': f'{token}'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_me(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        serializer = MeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Вы не авторизованы',
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
def set_password(request):
    serializer = PasswordSerializer(data=request.data)
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    if serializer.is_valid():
        if request.user.is_authenticated:
            user = get_object_or_404(
                User, id=request.user.id
            )
            if user.password != current_password:
                return Response(
                    'Не верный пароль',
                    status=status.HTTP_400_BAD_REQUEST
                )
            User.objects.filter(id=request.user.id).update(
                password=new_password
            )
            return Response(
                'Пароль изменен',
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
