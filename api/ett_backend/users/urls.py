from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserProfileView

urlpatterns = [
    path("api/member/profile/", UserProfileView.as_view(), name="user-profile"),
]
