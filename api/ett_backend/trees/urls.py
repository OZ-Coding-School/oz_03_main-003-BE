from django.urls import path

from trees.views import TreeCreateView, TreeEmotionListView, TreeEmotionRetrieveView, TreeListView, TreeUpdateDeleteView

urlpatterns = [
    path("new", TreeCreateView.as_view(), name="tree_create_view"),
    path("", TreeListView.as_view(), name="tree_list_retrieve_view"),
    path("<uuid:tree_uuid>", TreeUpdateDeleteView.as_view(), name="tree_update_delete_view"),
    path("emotion", TreeEmotionListView.as_view(), name="tree_emotion_list_view"),
    path("emotion/<uuid:tree_uuid>", TreeEmotionRetrieveView.as_view(), name="tree_emotion_retrieve_view"),
]
