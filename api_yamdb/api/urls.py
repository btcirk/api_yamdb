from django.urls import path, include
from rest_framework import routers

from .views import UsersViewSet
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'v1/users', UsersViewSet, basename='users')
router.register(r'v1/titles', TitleViewSet)
router.register(r'v1/genres', GenreViewSet, basename='genres')
router.register(r'v1/categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/', include('users.urls')),
]
