from django.forms import SlugField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import datetime as dt

from reviews.models import Title, Genre, Category


class CategorySerializer(serializers.ModelSerializer):
    slug = SlugField(
        validators = [
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Поле slug каждой категории должно быть уникальным'
            )
        ]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerilizer(serializers.ModelSerializer):
    slug = SlugField(
        validators = [
            UniqueValidator(
                queryset=Genre.objects.all(),
                message='Поле slug каждой категории должно быть уникальным'
            )
        ]
    )
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerilizer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Год выпуска не может быть больше текущего!')
        return value

    def create(self, validated_data):
        pass
