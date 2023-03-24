import django_filters

from food.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """Класс FilterSet для фильтрации рецепта."""
    tags = django_filters.CharFilter(
        field_name='tags__slug',
    )
    is_favorited = django_filters.NumberFilter(
        method='filter_favorited'
    )

    def filter_favorited(self, queryset, name, value):
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
        fields = ('tags', 'author',)
