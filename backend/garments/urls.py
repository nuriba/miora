from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GarmentViewSet, BrandSizeChartViewSet

app_name = 'garments'

router = DefaultRouter()
router.register('garments', GarmentViewSet, basename='garment')
router.register('size-charts', BrandSizeChartViewSet, basename='size-chart')

urlpatterns = [
    path('', include(router.urls)),
]