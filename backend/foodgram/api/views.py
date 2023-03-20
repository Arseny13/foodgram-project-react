from rest_framework import viewsets
from api.mixins import CreateListRetrieveViewSet
from users.models import User
from api.serializers import UserSerializer


class UserViewSet(CreateListRetrieveViewSet):
    """Вьюсет для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
