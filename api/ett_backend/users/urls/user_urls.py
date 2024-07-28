from django.urls import path

from users.views.user_crud_view import (
    SwitchUserAuthorizationView,
    UserListForAdmin,
    UserProfileView,
    UserRetrieveUpdateDeleteAdminView,
)

urlpatterns = [
    path("/profile", UserProfileView.as_view(), name="user_profile"),
    path("", UserListForAdmin.as_view(), name="user_list"),
    path("/<uuid:user_uuid>", UserRetrieveUpdateDeleteAdminView.as_view(), name="user_update"),
    path("/state/<uuid:user_uuid>", SwitchUserAuthorizationView.as_view(), name="switch_user_authorization"),
]
