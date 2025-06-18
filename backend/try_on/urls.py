from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TryOnSessionViewSet, OutfitViewSet, TryOnView

app_name = 'try_on'

router = DefaultRouter()
router.register('sessions', TryOnSessionViewSet, basename='tryon-session')
router.register('outfits', OutfitViewSet, basename='outfit')

urlpatterns = [
    path('', include(router.urls)),
    path('try-on/', TryOnView.as_view(), name='enhanced_try_on'),
]