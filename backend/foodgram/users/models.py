from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

USER = 'user'
ADMIN = 'admin'

CHOICES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор')
)


class CustomUserManager(UserManager):
    """Получения email."""
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username})
            | Q(**{self.model.EMAIL_FIELD: username})
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
    password = models.CharField(
        'Пароль',
        max_length=150
    )
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=15,
        default=USER,
    )

    objects = CustomUserManager()

    USERNAME_FIELDS = 'email'

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
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Класс Meta для Subscription описание метаданных."""
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'subscriber'),
                name="unique_subscriber_user"
            ),
        )

    def clean(self):
        if self.user == self.subscriber:
            raise ValidationError('нельзя на себя')

    def __str__(self) -> str:
        return f'{self.user.username} {self.subscriber.username}'
