from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import TryOnSession, TryOnSessionGarment, Outfit, OutfitGarment
from avatars.models import Avatar
from garments.models import Garment
from .serializers import (
    TryOnSessionSerializer,
    TryOnSessionCreateSerializer,
    OutfitSerializer,
    OutfitCreateFromSessionSerializer
)
from .services import VirtualTryOnService
from recommendations.services import SizeRecommendationService
from common.services.flora_fauna_service import FloraFaunaService
from common.services.revery_ai_service import ReveryAIService


class TryOnSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for virtual try-on sessions."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TryOnSessionSerializer
    
    def get_queryset(self):
        return TryOnSession.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Create a new try-on session."""
        serializer = TryOnSessionCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Create session
            session = TryOnSession.objects.create(
                user=request.user,
                avatar_id=serializer.validated_data['avatar_id'],
                session_name=serializer.validated_data.get('session_name', '')
            )
            
            # Add garments
            for garment_data in serializer.validated_data['garments']:
                TryOnSessionGarment.objects.create(
                    session=session,
                    garment_id=garment_data['garment_id'],
                    layer_order=garment_data['layer_order'],
                    selected_size=garment_data.get('selected_size', '')
                )
            
            # Run virtual try-on simulation
            try_on_service = VirtualTryOnService()
            results = try_on_service.simulate(session)
            
            # Update session with results
            session.fit_score = results.get('overall_fit_score')
            session.confidence_level = results.get('confidence')
            session.save()
            
            # Get size recommendations
            recommendation_service = SizeRecommendationService()
            for session_garment in session.garments.all():
                recommendation = recommendation_service.get_recommendation(
                    avatar=session.avatar,
                    garment=session_garment.garment
                )
                session_garment.fit_score = recommendation.get('fit_score')
                session_garment.save()
                
                if not session_garment.selected_size:
                    session_garment.selected_size = recommendation.get('recommended_size', '')
                    session_garment.save()
        
        # Return session with garments
        return Response(
            TryOnSessionSerializer(session).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def update_garment_size(self, request, pk=None):
        """Update selected size for a garment in the session."""
        session = self.get_object()
        garment_id = request.data.get('garment_id')
        new_size = request.data.get('size')
        
        if not garment_id or not new_size:
            return Response({
                'detail': 'garment_id and size are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session_garment = session.garments.get(garment__id=garment_id)
            session_garment.selected_size = new_size
            session_garment.save()
            
            # Recalculate fit score
            recommendation_service = SizeRecommendationService()
            new_score = recommendation_service.calculate_fit_score(
                session.avatar,
                session_garment.garment,
                new_size
            )
            session_garment.fit_score = new_score
            session_garment.save()
            
            return Response({
                'detail': 'Size updated successfully.',
                'new_fit_score': new_score
            })
        except TryOnSessionGarment.DoesNotExist:
            return Response({
                'detail': 'Garment not found in session.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def save_as_outfit(self, request, pk=None):
        """Save try-on session as outfit."""
        session = self.get_object()
        serializer = OutfitCreateFromSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Create outfit
            outfit = Outfit.objects.create(
                user=request.user,
                avatar=session.avatar,
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', ''),
                privacy_level=serializer.validated_data['privacy_level'],
                is_favorite=serializer.validated_data['is_favorite']
            )
            
            # Copy garments from session
            for session_garment in session.garments.all():
                OutfitGarment.objects.create(
                    outfit=outfit,
                    garment=session_garment.garment,
                    layer_order=session_garment.layer_order,
                    selected_size=session_garment.selected_size
                )
        
        return Response(
            OutfitSerializer(outfit).data,
            status=status.HTTP_201_CREATED
        )


class OutfitViewSet(viewsets.ModelViewSet):
    """ViewSet for outfit management."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OutfitSerializer
    
    def get_queryset(self):
        queryset = Outfit.objects.filter(user=self.request.user)
        
        # Filter by privacy level
        privacy = self.request.query_params.get('privacy')
        if privacy:
            queryset = queryset.filter(privacy_level=privacy)
        
        # Filter favorites
        if self.request.query_params.get('favorites') == 'true':
            queryset = queryset.filter(is_favorite=True)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle outfit favorite status."""
        outfit = self.get_object()
        outfit.is_favorite = not outfit.is_favorite
        outfit.save()
        
        return Response({
            'detail': 'Favorite status updated.',
            'is_favorite': outfit.is_favorite
        })
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate an outfit."""
        original = self.get_object()
        
        # Create new outfit
        outfit = Outfit.objects.create(
            user=request.user,
            avatar=original.avatar,
            name=f"{original.name} (Copy)",
            description=original.description,
            privacy_level='private',
            is_favorite=False
        )
        
        # Copy garments
        for garment in original.garments.all():
            OutfitGarment.objects.create(
                outfit=outfit,
                garment=garment.garment,
                layer_order=garment.layer_order,
                selected_size=garment.selected_size
            )
        
        return Response(
            OutfitSerializer(outfit).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def try_on(self, request, pk=None):
        """Create a try-on session from outfit."""
        outfit = self.get_object()
        
        # Create new session
        session = TryOnSession.objects.create(
            user=request.user,
            avatar=outfit.avatar,
            session_name=f"Try on: {outfit.name}"
        )
        
        # Copy garments
        for outfit_garment in outfit.garments.all():
            TryOnSessionGarment.objects.create(
                session=session,
                garment=outfit_garment.garment,
                layer_order=outfit_garment.layer_order,
                selected_size=outfit_garment.selected_size
            )
        
        return Response({
            'detail': 'Try-on session created.',
            'session_id': str(session.id)
        })


class TryOnView(APIView):
    """Enhanced virtual try-on with Flora Fauna (primary) and Revery AI (fallback)."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        avatar_id = request.data.get("avatar_id")
        garment_id = request.data.get("garment_id")
        
        if not avatar_id or not garment_id:
            return Response(
                {"error": "avatar_id and garment_id are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        avatar = get_object_or_404(Avatar, id=avatar_id, user=request.user)
        garment = get_object_or_404(Garment, id=garment_id)

        # Try Flora Fauna first
        flora = FloraFaunaService()
        try:
            result = flora.create_try_on(
                model_image=avatar.full_body_image_url,
                garment_image=getattr(garment, 'cleaned_image_url', garment.image_url),
                garment_type=garment.category
            )
        except Exception as e:
            # Fallback to Revery AI
            try:
                revery = ReveryAIService()
                result = revery.try_on(
                    avatar.full_body_image_url,
                    getattr(garment, 'cleaned_image_url', garment.image_url),
                    garment.category
                )
            except Exception as fallback_error:
                return Response(
                    {"error": f"Both services failed: {str(e)}, {str(fallback_error)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Save the result (you may need to create TryOnResult model)
        return Response({
            'image_url': result.get("output_url") or result.get("result_url"),
            'avatar_id': str(avatar.id),
            'garment_id': str(garment.id)
        }, status=status.HTTP_200_OK)
