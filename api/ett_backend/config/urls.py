from django.urls import include, path

urlpatterns = [
    path("api/health", include("common.urls")),
    path("api/dialog", include("dialog.urls")),
    path("api/chat", include("chatroom.urls")),
    path("api/auth", include("users.urls.auth_urls")),
    path("api/user", include("users.urls.user_urls")),
    path("api/forest", include("forest.urls")),
    path("api/tree", include("trees.urls")),
]
