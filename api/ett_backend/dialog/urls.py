from django.urls import path

from dialog.views import AIAppliedStateView, AIMessageView, DialogListView, UserMessageView

urlpatterns = [
    path("/message/user/<uuid:chat_room_uuid>", UserMessageView.as_view(), name="user_message"),
    path("/message/ai/<uuid:chat_room_uuid>", AIMessageView.as_view(), name="ai_message"),
    path("/ai/<uuid:message_uuid>", AIAppliedStateView.as_view(), name="ai_applied_state"),
    path("/<uuid:chat_room_uuid>", DialogListView.as_view(), name="dialog_list"),
]
