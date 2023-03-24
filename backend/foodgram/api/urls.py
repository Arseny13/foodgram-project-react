from django.urls import include, path
from rest_framework import routers
from api.views import (
    UserViewSet, get_me, set_password,
    TagViewSet, IngredientViewSet, CustomGetView,
    get_subscription, SubscribeViewSet,
    FavoriteViewSet, RecipeViewSet,
    ShoppingCartViewSet, get_ShoppingCart
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

router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)

router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)


router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shoppingcart'
)

router_v1.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)


urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        get_ShoppingCart,
        name='get_ShoppingCart'
    ),
    path('users/subscriptions/', get_subscription, name='subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/login/', CustomGetView.as_view(), name='login'),
    path('users/me/', get_me, name='me'),
    path('users/set_password/', set_password, name='set_password'),
    path('', include(router_v1.urls)),
]
