from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, mixins, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Title, Review, Comment, Genre, Category

from .serializers import TitleSerializer, TitleSerializerPost
from .serializers import ReviewSerializer, CommentSerializer
from .serializers import GenreSerilizer, CategorySerializer, UserSerializer
from .permissions import IsAdminOrReadOnlyPermission, IsAdminPermission
from .permissions import AuthorOrReadOnly, ReadOnly, OpenAll, IsAdminOrSuperuserPermission
from .permissions import OnlyAuthenticated, AuthorizedPermission

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, url_path='me', methods=['get', 'patch'],
            permission_classes = [AuthorizedPermission]
            )
    def me(self, request):
        user = User.objects.get(username=request.user)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerilizer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year')

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleSerializer
        return TitleSerializerPost


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    @staticmethod
    def rating_calculation(serializer, update):
        title_id = serializer.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if title.rating is None:
            title.rating = 0
        score = serializer.validated_data['score']
        count = Review.objects.filter(title__pk=title_id).count()
        if update:
            review_id = serializer.context['view'].kwargs['pk']
            review = get_object_or_404(Review, pk=review_id)
            score_old = review.score
            rating_new = (title.rating * count + score - score_old) / (count)
        else:
            rating_new = (title.rating * count + score) / (count + 1)
        title.rating = round(rating_new)
        title.save()

    def perform_create(self, serializer):
        title_id = serializer.context['view'].kwargs['title_id']
        self.rating_calculation(serializer, False)
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title, pk=title_id))

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
                        review=get_object_or_404(Review, pk=review_id))

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])

    def get_permissions(self):

        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
