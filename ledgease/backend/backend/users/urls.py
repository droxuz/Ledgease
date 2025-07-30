from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('portfolio/', MyTokenObtainPairView.as_view(), name='portfolio'),  # Example path for portfolio
    path('profile/', MyTokenObtainPairView.as_view(), name='profile'),  # Example path for profile
]