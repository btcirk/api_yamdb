from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'a'
    MODERATOR = 'm'
    USER = 'u'

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )
    role = models.CharField('Роль пользователя', max_length=1, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField('Биография', blank=True,)
