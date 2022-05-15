from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Review, Comment, Genre, Category
from users.models import User
from .serializers import TitleSerializer, ReviewSerializer, CommentSerializer
from .serializers import GenreSerilizer, CategorySerializer, UserSerializer
from .permissions import IsAdminOrReadOnlyPermission, AuthorOrReadOnly, ReadOnly, OpenAll
from .permissions import IsAdminPermission


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerilizer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination

    
class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (OpenAll,)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    @staticmethod
    def rating_calculation(serializer, update):
        title_id = serializer.context['view'].kwargs['title_id']
        title = Title.objects.get(pk=title_id)
        score = serializer.validated_data['score']
        count = Review.objects.filter(title__pk=title_id).count()
        if update:
            review_id = serializer.context['view'].kwargs['pk']
            review = Review.objects.get(pk=review_id)
            score_old = review.score
            rating_new = (title.rating * count + score - score_old) / (count)
        else:
            count = 1 if count == 0 else count
            rating_new = (title.rating * (count - 1) + score) / (count)
        title.rating = rating_new
        title.save()

    def perform_create(self, serializer):
        title_id = serializer.context['view'].kwargs['title_id']
        self.rating_calculation(serializer, False)
        serializer.save(author=self.request.user,
                        title=Title.objects.get(pk=title_id))

    def perform_update(self, serializer):
        self.rating_calculation(serializer, True)
        serializer.save()

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs['title_id'])

    def get_permissions(self):

        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        review_id = serializer.context['view'].kwargs['review_id']
        serializer.save(author=self.request.user,
                        review=Review.objects.get(pk=review_id))

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])

    def get_permissions(self):

        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
