from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from forest.models import Forest
from forest.serializers import ForestCreateSerializer, ForestRetreiveSerializer, ForestUpdateSerializer
from users.serializers import EmptySerializer


class ForestCreateView(CreateAPIView):
    serializer_class = ForestCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={"user_uuid": request.user.uuid})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            data={"forest_uuid": Forest.objects.filter(user=request.user).first().forest_uuid},
            status=status.HTTP_201_CREATED,
        )


class ForestRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "forest_uuid"
    queryset = Forest.objects.all()

    def get(self, request, *args, **kwargs):
        forest = Forest.objects.filter(user=request.user).first()
        if not forest:
            return Response({"error": "Forest not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ForestRetreiveSerializer(forest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        forest_uuid = kwargs.get(self.lookup_field)
        forest = Forest.objects.filter(forest_uuid=forest_uuid, user=request.user).first()
        if not forest:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ForestUpdateSerializer(instance=forest, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        forest_uuid = kwargs.get(self.lookup_field)
        forest = get_object_or_404(Forest, forest_uuid=forest_uuid, user=request.user)
        self.perform_destroy(instance=forest)
        return Response(status=status.HTTP_204_NO_CONTENT)
