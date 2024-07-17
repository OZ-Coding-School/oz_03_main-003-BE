from django.urls import path

from dialog.views import AIMessageRetrieveView, UserMessageListView, UserMessagePostView, UserMessageRetrieveView

from . import views

urlpatterns = [
    path("messages/list", UserMessageListView.as_view(), name="get_user_message_list"),
    path("messages/ai", AIMessageRetrieveView.as_view(), name="get_ai_generate_response"),
    path("messages/user", UserMessageRetrieveView.as_view(), name="get_user_message"),
    path("send", UserMessagePostView.as_view(), name="user-message-send"),
]
