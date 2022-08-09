from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField('Роль пользователя',
                            max_length=10,
                            choices=ROLE_CHOICES,
                            default=USER)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
