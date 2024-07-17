from django.urls import path

from users.views.google_auth_view import UserGoogleLoginCallbackView, UserGoogleLoginView
# from users.views.user_auth_view import UserLogoutView, UserDeleteView

urlpatterns = [
    path("google/login", UserGoogleLoginView.as_view(), name="google_login"),
    path("google/callback", UserGoogleLoginCallbackView.as_view(), name="google_callback"),
    # path("logout", UserLogoutView.as_view(), name="logout"),
    # path("delete", UserDeleteView.as_view(), name="user_delete"),
    # path("profile", UserProfileView.as_view()),
    # path("refresh", CustomUserTokenRefreshView.as_view()),
]
