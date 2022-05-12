from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Review, Comment  # ,Genre, Category


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
    # author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


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
