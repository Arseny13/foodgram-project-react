from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'

CHOICES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор')
)


class User(AbstractUser):
    """Класс пользователя."""
    username = models.CharField(
        'Юзернейм пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=15,
        default=USER,
    )

    @property
    def is_user(self):
        """Проверяет, если пользователь Юзер."""
        return self.role == USER

    @property
    def is_admin(self):
        """Проверяет, если пользователь Администратор."""
        return self.role == ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)


class Subscription(models.Model):
    """Класс подписок."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Класс Meta для Review описание метаданных."""
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'subscriber'),
                name="unique_subscriber_user"
            ),
        )

    def __str__(self) -> str:
        return self.user.username
