from django.urls import path

from forest.views import (
    ForestCreateView,
    ForestReceiveView,
    ForestDeleteView,
)

urlpatterns = [
    path("create", ForestCreateView.as_view(), name="forest_create"),
    path("get", ForestReceiveView.as_view(), name="forest_receive"),
    path("delete", ForestDeleteView.as_view(), name="forest_delete"),
]
