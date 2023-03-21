from django.db import models
from users.models import User


class Tag(models.Model):
    """Класс тега."""
    name = models.CharField(
        'Название тега',
        max_length=100,
        help_text='Введите название тега',
    )
    color = models.CharField(max_length=100,)
    slug = models.SlugField(
        'Cлаг тега',
        unique=True,
    )


class Ingredient(models.Model):
    """Класс ингридиента."""
    name = models.CharField(
        'Название ингридиента',
        max_length=100,
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.CharField(
        'Единицы измерения ингридиента',
        max_length=100,
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
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        '',
        blank=True,
        upload_to=''
    )
    text = models.TextField(
        'Описание рецепта',
    )
    tag = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        help_text='Введите время'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )


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
    amount = models.PositiveSmallIntegerField(
        'Количество ингридиента',
        help_text='Введите количество ингридиента'
    )

    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
