from django.urls import path

from .views import ForestCreateView, ForestDeleteView, ForestRetrieveView

urlpatterns = [
    path("forest/<uuid:uuid>/", ForestRetrieveView.as_view(), name="forest-detail"),
    path("forest/create/<uuid:uuid>/", ForestCreateView.as_view(), name="forest-create"),
    path("forest/delete/", ForestDeleteView.as_view(), name="forest-delete"),
]
