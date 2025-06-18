from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Outfit Posts URLs
    path('posts/', views.OutfitPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.OutfitPostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', views.OutfitPostLikeView.as_view(), name='post-like'),
    path('posts/<int:pk>/share/', views.OutfitPostShareView.as_view(), name='post-share'),
    
    # Style Challenges URLs
    path('challenges/', views.StyleChallengeListCreateView.as_view(), name='challenge-list-create'),
    path('challenges/<int:pk>/', views.StyleChallengeDetailView.as_view(), name='challenge-detail'),
    path('challenges/<int:pk>/join/', views.ChallengeJoinView.as_view(), name='challenge-join'),
    path('challenges/<int:pk>/submit/', views.ChallengeSubmitView.as_view(), name='challenge-submit'),
] 