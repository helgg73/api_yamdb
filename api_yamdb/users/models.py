from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F
from django.db.models.constraints import CheckConstraint


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
    )

    email = models.EmailField('Адрес email', unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль', max_length=20,
                            choices=CHOISES, default='user')

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
