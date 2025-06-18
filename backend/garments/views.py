from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Garment, GarmentProcessingLog, BrandSizeChart
from .serializers import (
    GarmentSerializer, 
    GarmentUploadSerializer,
    GarmentProcessingLogSerializer,
    BrandSizeChartSerializer
)
from .tasks import process_garment_image
import uuid


class GarmentViewSet(viewsets.ModelViewSet):
    """ViewSet for garment management."""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        queryset = Garment.objects.filter(user=self.request.user)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by processing status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(processing_status=status)
        
        # Search by name or brand
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(brand__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'upload':
            return GarmentUploadSerializer
        return GarmentSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Include processing logs if requested
        if self.request.query_params.get('include_logs') == 'true':
            context['include_logs'] = True
        return context
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload a new garment."""
        serializer = GarmentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save uploaded image temporarily
        image = serializer.validated_data.pop('image')
        image_path = f'garments/temp/{uuid.uuid4()}_{image.name}'
        
        # Create garment record
        garment = Garment.objects.create(
            user=request.user,
            original_image_url=image_path,
            processing_status='pending',
            **serializer.validated_data
        )
        
        # Create processing log
        GarmentProcessingLog.objects.create(
            garment=garment,
            processing_step='upload',
            status='completed'
        )
        
        # Queue processing task
        task = process_garment_image.delay(garment.id, image)
        
        return Response({
            'garment': GarmentSerializer(garment).data,
            'task_id': task.id,
            'detail': 'Garment uploaded and processing started.'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """Reprocess a failed garment."""
        garment = self.get_object()
        
        if garment.processing_status not in ['failed', 'completed']:
            return Response({
                'detail': 'Garment is already being processed.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset status
        garment.processing_status = 'processing'
        garment.save()
        
        # Queue reprocessing
        task = process_garment_image.delay(garment.id)
        
        return Response({
            'detail': 'Garment reprocessing started.',
            'task_id': task.id
        })
    
    @action(detail=True, methods=['get'])
    def processing_status(self, request, pk=None):
        """Get detailed processing status."""
        garment = self.get_object()
        logs = garment.processing_logs.all().order_by('-created_at')
        
        return Response({
            'garment_id': str(garment.id),
            'status': garment.processing_status,
            'logs': GarmentProcessingLogSerializer(logs, many=True).data
        })
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get available garment categories with counts."""
        categories = []
        for category, label in Garment.CATEGORY_CHOICES:
            count = self.get_queryset().filter(category=category).count()
            categories.append({
                'value': category,
                'label': label,
                'count': count
            })
        return Response(categories)


class BrandSizeChartViewSet(viewsets.ModelViewSet):
    """ViewSet for brand size charts."""
    queryset = BrandSizeChart.objects.all()
    serializer_class = BrandSizeChartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by brand
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__iexact=brand)
        
        # Filter by garment type
        garment_type = self.request.query_params.get('garment_type')
        if garment_type:
            queryset = queryset.filter(garment_type=garment_type)
        
        # Filter by gender
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        return queryset.order_by('brand', 'garment_type')
    
    @action(detail=False, methods=['get'])
    def brands(self, request):
        """Get list of brands with size charts."""
        brands = BrandSizeChart.objects.values_list('brand', flat=True).distinct()
        return Response(list(brands))