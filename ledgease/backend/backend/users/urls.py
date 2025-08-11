from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, registrationView, userProfileView, userPortfolioView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', registrationView.as_view(), name='register'),  
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', userProfileView.as_view(), name='profile'),  # Example path for profile
    path('portfolio/', userPortfolioView.as_view(), name='portfolio'),  # Example path for portfolio
]