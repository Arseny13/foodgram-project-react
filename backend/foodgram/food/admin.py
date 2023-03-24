from django.contrib import admin

from food.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'color',
                    'slug'
                    )
    list_editable = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто)))-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'measurement_unit'
                    )
    list_editable = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто)))-'


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 2


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'author',
                    'pub_date'
                    )
    list_editable = ('name',)
    inlines = (
        RecipeTagInline, RecipeIngredientInline,
    )
    search_fields = ('author', 'name', 'tag')
    empty_value_display = '-пусто)))-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'recipe',
                    )
    empty_value_display = '-пусто)))-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'recipe',
                    )
    empty_value_display = '-пусто)))-'
