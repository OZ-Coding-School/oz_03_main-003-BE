from django.urls import path

from users.views.google_auth_view import UserGoogleTokenReceiver
from users.views.user_auth_view import (
    UserDeleteView,
    UserLogoutView,
    UserProfileView,
    UserTokenRefreshView,
    UserTokenVerifyView,
)

urlpatterns = [
    path("/google/receiver", UserGoogleTokenReceiver.as_view(), name="google_receiver"),
    path("/token/verify", UserTokenVerifyView.as_view(), name="token_verify"),
    path("/token/refresh", UserTokenRefreshView.as_view(), name="token_refresh"),
    path("/logout", UserLogoutView.as_view(), name="user_logout"),
    path("/delete", UserDeleteView.as_view(), name="user_delete"),
    path("/profile", UserProfileView.as_view(), name="user_profile"),
]
