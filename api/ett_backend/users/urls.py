from django.urls import path

from users.views.google_auth_view import UserGoogleTokenReceiver
# from users.views.user_auth_view import UserLogoutView, UserDeleteView

urlpatterns = [
    path("google/receiver", UserGoogleTokenReceiver.as_view(), name="google_receiver"),
]
