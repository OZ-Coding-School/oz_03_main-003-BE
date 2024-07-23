from django.urls import path

from dialog.views import AIMessageRetrieveView, UserMessageCreateView

urlpatterns = [
    path("send", UserMessageCreateView.as_view(), name="send_user_message"),
    path("message/ai/<uuid:chat_room_uuid>", AIMessageRetrieveView.as_view(), name="retrieve_ai_message"),
]
