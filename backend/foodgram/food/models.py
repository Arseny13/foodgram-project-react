from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from colorfield.fields import ColorField

from users.models import User


class Tag(models.Model):
    """Класс тега."""
    name = models.CharField(
        'Название тега',
        unique=True,
        max_length=100,
        help_text='Введите название тега',
    )
    color = ColorField(unique=True)
    slug = models.SlugField(
        'Cлаг тега',
        unique=True,
    )

    class Meta:
        """Класс Meta для Tag описание метаданных."""
        ordering = ('id',)
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Класс ингридиента."""
    name = models.CharField(
        'Название ингридиента',
        max_length=100,
        unique=True,
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.CharField(
        'Единицы измерения ингридиента',
        max_length=20,
        help_text='Введите eдиницу измерения ингридиента'
    )

    class Meta:
        """Класс Meta для Ingredient описание метаданных."""
        ordering = ('id',)
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Класс рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        'Картинка рецепта',
        blank=True,
        upload_to='recipe/',
    )
    text = models.TextField(
        'Описание рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        help_text='Введите время',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(1440)
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        """Класс Meta для Recipe описание метаданных."""
        ordering = ('id',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return self.name


class TagRecipe(models.Model):
    """Класс cвязи тега и рецепта."""
    tag = models.ForeignKey(
        Tag,
        verbose_name='тег',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        """Класс Meta для TagRecipe описание метаданных."""
        ordering = ('id',)
        verbose_name = 'тег_рецепт'
        verbose_name_plural = 'теги_рецепты'

    def __str__(self) -> str:
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    """Класс cвязи ингридиента и рецепта."""
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ингридиент',
        related_name='ingredient',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        related_name='recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингридиента',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(100)
        ),
        help_text='Введите количество ингридиента'
    )

    class Meta:
        """Класс Meta для IngredientRecipe описание метаданных."""
        ordering = ('id',)
        verbose_name = 'ингридиент_рецепт'
        verbose_name_plural = 'ингридиенты_рецепты'

    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    """Класс избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        """Класс Meta для Favorite описание метаданных."""
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-recipe__pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name="unique_recipe_user_favorite"
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    """Класс списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт'
    )

    class Meta:
        """Класс Meta для ShoppingCart описание метаданных."""
        verbose_name = 'СписокПокупок'
        verbose_name_plural = 'СпискиПокупок'
        ordering = ('-recipe__pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name="unique_recipe_user_shoppingcart"
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'
