from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Avatar, AvatarGenerationLog
from .serializers import AvatarSerializer, AvatarCreateSerializer, AvatarGenerationLogSerializer
from .tasks import generate_avatar_from_photo


class AvatarViewSet(viewsets.ModelViewSet):
    """ViewSet for avatar management."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Avatar.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AvatarCreateSerializer
        return AvatarSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        """Set avatar as active."""
        avatar = self.get_object()
        
        # Deactivate all other avatars
        Avatar.objects.filter(user=request.user).exclude(pk=avatar.pk).update(is_active=False)
        
        # Activate this avatar
        avatar.is_active = True
        avatar.save()
        
        return Response({
            'detail': 'Avatar set as active.',
            'avatar': AvatarSerializer(avatar).data
        })
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the active avatar."""
        try:
            avatar = Avatar.objects.get(user=request.user, is_active=True)
            serializer = self.get_serializer(avatar)
            return Response(serializer.data)
        except Avatar.DoesNotExist:
            return Response({
                'detail': 'No active avatar found.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def generate_from_photo(self, request, pk=None):
        """Generate 3D avatar from photo."""
        avatar = self.get_object()
        photo = request.FILES.get('photo')
        
        if not photo:
            return Response({
                'detail': 'Photo is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create generation log
        log = AvatarGenerationLog.objects.create(
            avatar=avatar,
            generation_method='photo',
            source_images=[photo.name]
        )
        
        # Queue async task for avatar generation
        task = generate_avatar_from_photo.delay(avatar.id, photo)
        
        return Response({
            'detail': 'Avatar generation started.',
            'task_id': task.id,
            'log_id': str(log.id)
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=True, methods=['get'])
    def generation_logs(self, request, pk=None):
        """Get generation logs for avatar."""
        avatar = self.get_object()
        logs = avatar.generation_logs.all().order_by('-created_at')
        serializer = AvatarGenerationLogSerializer(logs, many=True)
        return Response(serializer.data)
