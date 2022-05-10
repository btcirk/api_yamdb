from rest_framework.routers import DefaultRouter
from django.urls import include, path
# from .views import PostViewSet, GroupViewSet, CommentsViewSet, FollowViewSet

router = DefaultRouter()

# router.register('v1/posts', PostViewSet)
# router.register('v1/groups', GroupViewSet)
# router.register('v1/follow', FollowViewSet)


# router.register(r'v1/posts/(?P<post_id>\d+)/comments', CommentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]