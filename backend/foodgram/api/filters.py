import django_filters

from rest_framework import filters

from food.models import Recipe


class IngredientSearchFilter(filters.SearchFilter):
    search_param = "name"


class RecipeFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации рецепта."""
    tags = django_filters.CharFilter(
        field_name='tags__slug',
    )
    is_favorited = django_filters.NumberFilter(
        method='filter_favorited', label='is_favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_shopping_cart',
        label='is_in_shopping_cart',
    )

    def filter_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == 1:
                return queryset.filter(
                    shoppingcart__user=self.request.user
                )
            if value == 0:
                return queryset.exclude(
                    shoppingcart__user=self.request.user
                )
        return queryset

    def filter_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == 1:
                return queryset.filter(
                    favorites__user=self.request.user
                )
            if value == 0:
                return queryset.exclude(
                    favorites__user=self.request.user
                )
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'tags', 'is_favorited',
            'author', 'is_in_shopping_cart'
        )
