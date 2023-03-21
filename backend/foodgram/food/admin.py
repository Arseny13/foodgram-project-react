from django.contrib import admin
from food.models import Tag, Recipe, Ingredient


@admin.register(Tag)
class IngredientAdmin(admin.ModelAdmin):
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
    model = Recipe.tag.through
    extra = 2


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'author',
                    'pub_date'
                    )
    list_editable = ('title',)
    inlines = (
        RecipeTagInline, RecipeIngredientInline,
    )
    search_fields = ('author', 'title', 'tag')
    empty_value_display = '-пусто)))-'
