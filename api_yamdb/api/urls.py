from django.urls import path, include
from rest_framework import routers

from .views import UsersViewSet, CommentsViewSet, ReviewsViewSet, TitlesViewSet


router = routers.DefaultRouter()
router.register(r'v1/users', UsersViewSet, basename='users')

router.register('v1/titles', TitlesViewSet, basename='titles')
router.register(r'v1/titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/', include('users.urls')),
]
