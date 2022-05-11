from django.urls import path, include
from rest_framework import routers

from .views import UsersViewSet


router = routers.DefaultRouter()
router.register(r'v1/users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/', include('users.urls')),
]
