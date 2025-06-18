from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TryOnSessionViewSet, OutfitViewSet

app_name = 'try_on'

router = DefaultRouter()
router.register('sessions', TryOnSessionViewSet, basename='tryon-session')
router.register('outfits', OutfitViewSet, basename='outfit')

urlpatterns = [
    path('', include(router.urls)),
]