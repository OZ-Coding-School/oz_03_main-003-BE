from django.urls import path

from trees.views import (
    TreeListCreateView,
    TreeEmotionListView,
)

urlpatterns = [
    path("", TreeListCreateView.as_view(), name="tree_list_create_view"),
    path("emotion", TreeEmotionListView.as_view(), name="tree_emotion_view"),
]
