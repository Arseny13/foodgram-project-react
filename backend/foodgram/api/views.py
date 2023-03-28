from api.filters import RecipeFilter
from api.mixins import (CreateDestroyViewSet, CreateListRetrieveViewSet,
                        ListRetrieveViewSet)
from api.permissions import IsReadOnly
from api.serializers import (FavoriteSerializer, GetShoppingCartSerializer,
                             IngredientSerializer, MeSerializer,
                             MyUserSerializer, PasswordSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             ShoppingCartSerializer, SubscriptionSerializer,
                             TagSerializer)
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from food.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Subscription, User


class UserViewSet(CreateListRetrieveViewSet):
    """Вьюсет для пользователей."""
    queryset = User.objects.all()
    serializer_class = MyUserSerializer

    def perform_create(self, serializer):
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class TagViewSet(ListRetrieveViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    """Вьюсет для ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RecipeFilter
    permission_classes = (IsReadOnly,)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def get_serializer_class(self):
        """Метод изменения класса сериализера при разных методах."""
        if self.action in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )


class GetSubscription(APIView, LimitOffsetPagination):
    """Класс для переопределения запросов GET."""

    def get(self, request):
        """Получение подписок авторизаваного пользователя."""
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            quersy = user.follower.all()
            results = self.paginate_queryset(quersy, request, view=self)
            serializer = SubscriptionSerializer(
                results,
                many=True,
                context={'request': request}
            )

            return self.get_paginated_response(serializer.data)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )


class SubscribeViewSet(CreateDestroyViewSet):
    """Вьюсет для подписок."""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsReadOnly,)

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.request.user.follower.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['subscription_id'] = self.kwargs.get('user_id')
        return context

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
    """Вьюсет для избранного."""
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def delete(self, request, recipe_id):
        """Отписаться от автора."""
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id),
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_ShoppingCart(request):
    """Вьюха для получение списка покупок."""
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        serializer = GetShoppingCartSerializer(
            user.user.all(),
            context={'request': request}
        )
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="filename.txt"'
        response.write(serializer.data)
        return response
    return Response(
        'Вы не авторизованы',
        status=status.HTTP_401_UNAUTHORIZED
    )


class ShoppingCartViewSet(CreateDestroyViewSet):
    """Вьюсет для списка покупок."""
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsReadOnly,)

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    def get_queryset(self):
        return self.request.user.shoppingcart.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def delete(self, request, recipe_id):
        """Отписаться от автора."""
        shoppingcart = get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id),
        )
        shoppingcart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_me(request):
    """Вьюха для получение информации о текущем пользователе."""
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
    """Вьюха для изменения пароля."""
    serializer = PasswordSerializer(data=request.data)
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    if serializer.is_valid():
        if request.user.is_authenticated:
            user = get_object_or_404(
                User, id=request.user.id
            )
            if check_password(current_password, user.password):
                User.objects.filter(id=request.user.id).update(
                    password=make_password(new_password)
                )
                return Response(
                    'Пароль изменен',
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                'Не верный пароль',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
