from django.urls import path

from forest.views import (
    ForestCreateView,
    ForestRetrieveUpdateDeleteView,
)

urlpatterns = [
    path("new", ForestCreateView.as_view(), name="forest_create"),
    path("", ForestRetrieveUpdateDeleteView.as_view(), name="forest_receive"),
    path("<uuid:forest_uuid>", ForestRetrieveUpdateDeleteView.as_view(), name="forest_update_delete"),
]
