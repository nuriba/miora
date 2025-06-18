from django.contrib import admin
from .models import Garment, GarmentProcessingLog, BrandSizeChart

@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'brand', 'processing_status', 'created_at']
    list_filter = ['category', 'processing_status', 'gender']
    search_fields = ['name', 'brand', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(BrandSizeChart)
class BrandSizeChartAdmin(admin.ModelAdmin):
    list_display = ['brand', 'garment_type', 'gender', 'size_system']
    list_filter = ['brand', 'garment_type', 'size_system']
    search_fields = ['brand']