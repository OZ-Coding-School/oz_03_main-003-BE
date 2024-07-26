from django.urls import path

from forest.views import ForestCreateView, ForestListAdminView, ForestRetrieveUpdateDeleteView, ForestUpdateAdminView

urlpatterns = [
    path("/new", ForestCreateView.as_view(), name="forest_create"),
    path("", ForestRetrieveUpdateDeleteView.as_view(), name="forest_receive"),
    path("/<uuid:forest_uuid>", ForestRetrieveUpdateDeleteView.as_view(), name="forest_update_delete"),
    path("/admin", ForestListAdminView.as_view(), name="admin_forest_list"),
    path("/admin/<uuid:forest_uuid>", ForestUpdateAdminView.as_view(), name="admin_forest_update"),
]
