from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import username_validator


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(
        'Имя пользователя, username',
        max_length=150,
        unique=True,
        help_text='Имя пользователя',
        validators=(username_validator,),
        error_messages={
            'unique': 'Имя пользователя занято',
        },
    )
    email = models.EmailField('Адрес email', unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль', max_length=20,
                            choices=ROLE_CHOISES, default='user')

    class Meta:
        ordering = ('role',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER
