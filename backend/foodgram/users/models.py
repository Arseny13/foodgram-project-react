from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Q

USER = 'user'
ADMIN = 'admin'

CHOICES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор')
)


class CustomUserManager(BaseUserManager):
    """Класс для создания обычного пользователя/суперпользователя."""

    def create_superuser(self, username, email, password, **kwargs):
        """
        Cоздает и сохраняет суперпользователя
        с указанным адресом электронной почты и паролем.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )

    def create_user(self, username, email, password=None, **kwargs):
        """
        Cоздает и сохраняет пользователя
        с указанным адресом электронной почты и паролем.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()
        return user

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

    REQUIRED_FIELDS = ('email',)
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
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        User,
        related_name='following',
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

    def __str__(self) -> str:
        return self.user.username
