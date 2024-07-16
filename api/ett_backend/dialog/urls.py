from django.urls import path

from . import views
from dialog.views import UserMessagePostView, AIMessageRetrieveView

urlpatterns = [
    # path("list", ChatRoomListView.as_view()),
    # path("list/<uuid:chat_room_uuid>", ChatRoomRetrieveView.as_view()),
    # path("create", ChatRoomCreateView.as_view()),
    # path("messages", ChatRoomMessagesListView.as_view()),
    path("messages/ai", AIMessageRetrieveView.as_view()),
    # path("messages/user", UserMessageRetrieveView.as_view()),
    path("send", UserMessagePostView.as_view()),
    # path("delete", ChatRoomDeleteView.as_view()),
]
