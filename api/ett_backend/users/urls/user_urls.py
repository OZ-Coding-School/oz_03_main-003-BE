from django.urls import path

from users.views.user_crud_view import SwitchUserAuthorizationView, UserProfileView, UserView

urlpatterns = [
    path("/profile", UserProfileView.as_view(), name="user_profile"),
    path("", UserView.as_view(), name="user_list"),
    path("/<uuid:user_uuid>", SwitchUserAuthorizationView.as_view(), name="switch_user_authorization"),
]
