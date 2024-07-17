from django.urls import path

from users.views import UserGoogleLoginCallbackView, UserGoogleLoginView

urlpatterns = [
    path("google/login", UserGoogleLoginView.as_view(), name="google_login"),
    path("google/callback", UserGoogleLoginCallbackView.as_view(), name="google_callback"),
    # path("logout", UserLogoutView.as_view()),
    # path("delete", UserDeleteView.as_view()),
    # path("profile", UserProfileView.as_view()),
    # path("refresh", CustomUserTokenRefreshView.as_view()),
]
