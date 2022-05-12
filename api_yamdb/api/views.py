from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from reviews.models import Title, Genre, Category

from .serializers import TitleSerializer, GenreSerilizer, CategorySerializer
from .permissions import IsAdminOrReadOnlyPermission


class UsersViewSet(viewsets.ModelViewSet):
    pass



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
