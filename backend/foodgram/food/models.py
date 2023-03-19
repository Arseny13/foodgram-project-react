from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    """Класс тега."""
    title = models.CharField(
        'Название тега',
        help_text='Введите название тега',
    )
    color = models.CharField()
    slug = models.SlugField(
        'Cлаг тега',
        unique=True,
    )


class Ingredient(models.Model):
    """Класс ингридиента."""
    title = models.CharField(
        'Название ингридиента',
        help_text='Введите название ингридиента',
    )
    count = models.PositiveSmallIntegerField(
        'Количество ингридиента',
        help_text='Введите количество ингридиента'
    )
    unit = models.CharField(
        'Единицы измерения ингридиента',
        help_text='Введите eдиницу измерения ингридиента'
    )


class Recipe(models.Model):
    """Класс рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='',
        help_text='',
    )
    image = models.ImageField(
        '',
        blank=True,
        upload_to=''
    )
    description = models.TextField(
        'Описание рецепта',
    )
    ingredient = models.ManyToManyField(
        Ingredient,

    )
    tag = models.ForeignKey(
        Tag,
        through='TagRecipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        through='IngredientRecipe'
    )
    time = models.TimeField()


class TagRecipe(models.Model):
    """Класс cвязи тега и рецепта."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    """Класс cвязи ингридиента и рецепта."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'
