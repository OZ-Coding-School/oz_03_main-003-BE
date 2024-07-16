from django.urls import path

from . import views
from dialog.views import UserMessagePostView, AIMessageRetrieveView, UserMessageRetrieveView, UserMessageListView

urlpatterns = [
    # path("list", ChatRoomListView.as_view()),
    # path("list/<uuid:chat_room_uuid>", ChatRoomRetrieveView.as_view()),
    # path("create", ChatRoomCreateView.as_view()),
    path("messages/list", UserMessageListView.as_view(), name="get_user_message_list"),
    path("messages/ai", AIMessageRetrieveView.as_view(), name="get_ai_generate_response"),
    path("messages/user", UserMessageRetrieveView.as_view(), name="get_user_message"),
    path("send", UserMessagePostView.as_view(), name="user-message-send"),
    # path("delete", ChatRoomDeleteView.as_view()),
]
