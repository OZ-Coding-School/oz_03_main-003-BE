from django.urls import path

from chatroom.views import (
    ChatRoomCreateView,
    ChatRoomDeleteView,
    ChatRoomListView,
    ChatRoomRetrieveView,
    ChatRoomUpdateView,
)

urlpatterns = [
    path("create", ChatRoomCreateView.as_view(), name="create_chat_room"),
    path("list", ChatRoomListView.as_view(), name="chat_room_list"),
    path("retrieve", ChatRoomRetrieveView.as_view(), name="chat_room_retrieve"),
    path("update", ChatRoomUpdateView.as_view(), name="chat_room_update"),
    path("delete", ChatRoomDeleteView.as_view(), name="chat_room_delete"),
]
