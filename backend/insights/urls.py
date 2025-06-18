from django.urls import path
from . import views

app_name = 'insights'

urlpatterns = [
    # Style Analytics
    path('analytics/', views.StyleAnalyticsView.as_view(), name='analytics'),
    path('analytics/update/', views.UpdateAnalyticsView.as_view(), name='analytics-update'),
    
    # Color Analytics
    path('colors/', views.ColorAnalyticsView.as_view(), name='color-analytics'),
    
    # Style Evolution
    path('evolution/', views.StyleEvolutionView.as_view(), name='style-evolution'),
    
    # Sustainability
    path('sustainability/', views.SustainabilityInsightsView.as_view(), name='sustainability'),
    
    # Wear Events
    path('wear-events/', views.WearEventListCreateView.as_view(), name='wear-events'),
    path('wear-events/<int:pk>/', views.WearEventDetailView.as_view(), name='wear-event-detail'),
    
    # Milestones
    path('milestones/', views.StyleMilestoneListView.as_view(), name='milestones'),
    
    # Trends
    path('trends/', views.TrendAnalysisListView.as_view(), name='trends'),
] 