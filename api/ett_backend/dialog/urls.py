from django.urls import path

from . import views

urlpatterns = [
    path("list", views.ChatRoomListCreateView.as_view(), name="Chat_list"),
    path("list/<int:chat_room_uuid>", views.UserDialogListCreateView.as_view(), name="specific_Chat_list"),
]
