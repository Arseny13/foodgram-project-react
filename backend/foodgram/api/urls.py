from django.urls import include, path
from rest_framework import routers
from api.views import (
    UserViewSet, get_me, set_password,
    TagViewSet, IngredientViewSet, CustomGetView
)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

router_v1.register(
    'tags',
    TagViewSet,
    basename='tags'
)

router_v1.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/login/', CustomGetView.as_view(), name='login'),
    path('users/me/', get_me, name='me'),
    path('users/set_password/', set_password, name='set_password'),
    path('', include(router_v1.urls)),
]
