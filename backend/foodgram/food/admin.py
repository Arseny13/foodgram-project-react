from django.contrib import admin
from food.models import Tag, Recipe, Ingredient

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
