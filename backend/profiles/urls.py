from django.urls import path
from .views import UserProfileDetailView, PublicProfileView

app_name = 'profiles'

urlpatterns = [
    path('me/', UserProfileDetailView.as_view(), name='my_profile'),
    path('<uuid:user_id>/', PublicProfileView.as_view(), name='public_profile'),
]