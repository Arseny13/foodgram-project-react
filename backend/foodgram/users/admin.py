from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email'
                    )
    list_editable = ('username',)
    search_fields = ('username',)
    empty_value_display = '-пусто)))-'


@admin.register(Subscription)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'subscriber'
                    )
    empty_value_display = '-пусто)))-'
