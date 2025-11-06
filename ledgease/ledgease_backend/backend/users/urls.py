from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, RegistrationView, UserProfileView, UserPortfolioView, UserUpdateView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegistrationView.as_view(), name='register'),  
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),  # Example path for profile
    path('profile/user-update/', UserUpdateView.as_view(),name='user-update'),  # Path for user update
    path('portfolio/', UserPortfolioView.as_view(), name='portfolio'),  # Example path for portfolio

]