
from django.forms import SlugField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

import datetime as dt

from reviews.models import Title, Genre, Category, Review, Comment


class CurrentTitleDefault(object):

    def set_context(self, serializer_field):
        self.title_id = serializer_field.context['view'].kwargs['title_id']

    def __call__(self):
        return self.title_id


class CurrentCommentDefault(object):

    def set_context(self, serializer_field):
        self.review_id = serializer_field.context['view'].kwargs['review_id']

    def __call__(self):
        return self.review_id


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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        fields = '__all__'
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = serializers.HiddenField(default=CurrentCommentDefault())

    class Meta:
        fields = '__all__'
        model = Comment

        
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
