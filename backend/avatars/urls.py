from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvatarViewSet

app_name = 'avatars'

router = DefaultRouter()
router.register('', AvatarViewSet, basename='avatar')

urlpatterns = [
    path('', include(router.urls)),
]