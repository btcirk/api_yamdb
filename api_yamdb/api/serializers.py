from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Review, Comment  # ,Genre, Category


class CurrentTitleDefault(object):

    def set_context(self, serializer_field):
        self.title_id = serializer_field.context['view'].kwargs['title_id']

    def __call__(self):
        return self.title_id


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

    class Meta:
        fields = '__all__'
        model = Comment
# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username'
#     )

#     class Meta:
#         fields = '__all__'
#         model = Comment
#         read_only_fields = ('post',)


# class FollowSerializer(serializers.ModelSerializer):
#     user = SlugRelatedField(slug_field='username', read_only=True,
#                             default=serializers.CurrentUserDefault())
#     following = SlugRelatedField(slug_field='username',
#                                  queryset=User.objects.all())

#     class Meta:
#         model = Follow
#         fields = '__all__'
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following')
#             )
#         ]

#     def validate(self, data):
#         if not data['following']:
#             raise serializers.ValidationError('заполните поле following')
#         elif data['following'] == self._context['request'].user:
#             raise serializers.ValidationError('Подписаться на'
#                                               'самого себя невозможно')
#         return data


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
