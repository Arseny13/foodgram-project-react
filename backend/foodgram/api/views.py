from rest_framework import viewsets, filters, status
from api.mixins import CreateListRetrieveViewSet, ListRetrieveViewSet
from users.models import User
from food.models import Tag, Ingredient
from api.serializers import (
    UserSerializer, GetTokenSerializer,
    MeSerializer, PasswordSerializer,
    TagSerializer, IngredientSerializer
)
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from djoser.views import TokenCreateView


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
