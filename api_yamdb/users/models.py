from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (
    ADMIN, MODERATOR, ROLE_CHOISES, USERNAME_MAX_LENGTH, DEFAULT_ROLE,
    MAX_LENGTH_ROLE, USER_EMAIL_MAX_LENGTH
)
from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя, username',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Имя пользователя',
        validators=(validate_username,),
        error_messages={
            'unique': 'Имя пользователя занято',
        },
    )
    email = models.EmailField(
        'Адрес email',
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOISES, default=DEFAULT_ROLE
    )

    class Meta:
        ordering = ('role',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == ADMIN or self.is_staff
        )

    def __str__(self):
        return self.username
