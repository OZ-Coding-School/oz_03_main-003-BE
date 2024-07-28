from django.urls import path

from trees.views import (
    TreeCreateView,
    TreeEmotionListAdminView,
    TreeEmotionListView,
    TreeEmotionRetrieveUpdateView,
    TreeEmotionUpdateAdminView,
    TreeListAdminView,
    TreeListView,
    TreeRetrieveUpdateDeleteAdminView,
    TreeRetrieveUpdateDeleteView,
)

urlpatterns = [
    path("/new", TreeCreateView.as_view(), name="tree_create_view"),
    path("", TreeListView.as_view(), name="tree_list_retrieve_view"),
    path("/<uuid:tree_uuid>", TreeRetrieveUpdateDeleteView.as_view(), name="tree_retrieve_update_delete_view"),
    path("/emotion", TreeEmotionListView.as_view(), name="tree_emotion_list_view"),
    path(
        "/emotion/<uuid:tree_uuid>", TreeEmotionRetrieveUpdateView.as_view(), name="tree_emotion_retrieve_update_view"
    ),
    path("/admin", TreeListAdminView.as_view(), name="admin_tree_list_view"),
    path("/admin/<uuid:tree_uuid>", TreeRetrieveUpdateDeleteAdminView.as_view(), name="admin_tree_update_delete_view"),
    path("/admin/emotion", TreeEmotionListAdminView.as_view(), name="admin_tree_emotion_list_view"),
    path(
        "/admin/emotion/<uuid:tree_uuid>", TreeEmotionUpdateAdminView.as_view(), name="admin_tree_emotion_update_view"
    ),
]
