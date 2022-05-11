from rest_framework import viewsets
from reviews.models import Title, Review, Comment  # ,Genre, Category
from .serializers import TitleSerializer, ReviewSerializer, CommentSerializer
from .permissions import AuthorOrReadOnly, ReadOnly, OpenAll


class UsersViewSet(viewsets.ModelViewSet):
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (OpenAll,)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = serializer.context['view'].kwargs['title_id']
        serializer.save(author=self.request.user,
                        title=Title.objects.get(pk=title_id))

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs['title_id'])

    def get_permissions(self):

        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OpenAll,)
