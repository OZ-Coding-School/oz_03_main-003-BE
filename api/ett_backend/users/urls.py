from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserProfileView

urlpatterns = [
    # path("login", UserSocialLoginView.as_view()),
    # path("logout", UserLogoutView.as_view()),
    # path("delete", UserDeleteView.as_view()),
    # path("profile", UserProfileView.as_view()),
    # path("refresh", CustomUserTokenRefreshView.as_view()),
]
