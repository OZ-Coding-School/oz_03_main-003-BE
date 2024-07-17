from django.urls import path

from users.views.google_auth_view import UserGoogleLoginCallbackView, UserGoogleLoginView
from users.views.kakao_auth_view import UserKakaoLoginCallbackView, UserKakaoLoginView

urlpatterns = [
    path("google/login", UserGoogleLoginView.as_view(), name="google_login"),
    path("google/callback", UserGoogleLoginCallbackView.as_view(), name="google_callback"),
    # path("logout", UserLogoutView.as_view()),
    # path("delete", UserDeleteView.as_view()),
    # path("profile", UserProfileView.as_view()),
    # path("refresh", CustomUserTokenRefreshView.as_view()),
]
