from django.urls import path, include

from .views import RegisterUserView, CustomTokenRefreshView, CustomTokenObtainPairView, \
    PasswordChangeView

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register-user-v1'),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair-v1'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh-v1'),
    path('auth/change-password/', PasswordChangeView.as_view(), name='password-change'),
]
