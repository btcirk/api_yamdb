import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Genre, Category, Review, Comment
from users.models import User


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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerilizer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerilizer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    DefUser = serializers.CurrentUserDefault()
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          default=DefUser)

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
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.HiddenField(default=CurrentCommentDefault())

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
