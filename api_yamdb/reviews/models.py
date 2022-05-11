from django.db import models


class Genres(models.Model):
    """
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(
        verbose_name='Жанр произведения'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес для страницы жанр'
    )

    def __str__(self):
        return self.name


class Categories(models.Model):
    """
    Категории (типы) произведений ("Фильмы", "Книги" , "Музыка").
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Категория произведения'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес для страницы категории'
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    """
    Произведения, к которым пишут отзывы (определенный фильм,
    книга или песенка)
    """
    name = models.CharField()
    year = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name
