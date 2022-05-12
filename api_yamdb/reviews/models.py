from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint

User = get_user_model()


class Genre(models.Model):
    """
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Жанр произведения'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес для страницы жанр'
    )

    def __str__(self):
        return self.name


class Category(models.Model):
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


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определенный фильм,
    книга или песенка)
    """
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        # through='GenreTitle',
        related_name='titles',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    rating = models.IntegerField(blank=True, default=5)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.IntegerField(default=5,
                                validators=[MaxValueValidator(10),
                                            MinValueValidator(1)
                                            ])

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'title'],
                             name='unique_author_title')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
