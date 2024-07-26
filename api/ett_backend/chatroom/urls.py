from django.urls import path

from chatroom.views import (
    ChatRoomCreateView,
    ChatRoomListForAdminView,
    ChatRoomListView,
    ChatRoomRetrieveUpdateDeleteView,
)

urlpatterns = [
    path("/new", ChatRoomCreateView.as_view(), name="create_chat_room"),
    path("", ChatRoomListView.as_view(), name="chat_room_list"),
    path("/<uuid:chat_room_uuid>", ChatRoomRetrieveUpdateDeleteView.as_view(), name="chat_room_retrieve_update_delete"),
    path("/admin", ChatRoomListForAdminView.as_view(), name="admin_chat_room_list"),
]
