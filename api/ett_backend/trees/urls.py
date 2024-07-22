from django.urls import path

from trees.views import (
    TreeListCreateView,
    TreeUpdateDeleteView,
    TreeEmotionListView,
)

urlpatterns = [
    path("", TreeListCreateView.as_view(), name="tree_list_create_view"),
    path("<uuid:tree_uuid>", TreeUpdateDeleteView.as_view(), name="tree_update_delete_view"),
    path("emotion/", TreeEmotionListView.as_view(), name="tree_emotion_view"),
]
