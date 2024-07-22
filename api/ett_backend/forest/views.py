from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView

from forest.models import Forest
from forest.serializers import ForestCreateSerializer, ForestRetreiveSerializer, ForestDeleteSerializer


class ForestCreateView(GenericAPIView):
    serializer_class = ForestCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serlializer = self.get_serializer(data={"user_uuid": request.user.uuid})
        serlializer.is_valid(raise_exception=True)
        forest = serlializer.save()

        return Response(
            data={
                "forest_uuid": forest.forest_uuid,
            },
            status=status.HTTP_201_CREATED
        )


class ForestReceiveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        forest = Forest.objects.filter(user=user).first()
        if not forest:
            return Response({"error": "Forest not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ForestRetreiveSerializer(forest)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForestDeleteView(GenericAPIView):
    serializer_class = ForestDeleteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            forest = serializer.validated_data["forest"]
            with transaction.atomic():
                forest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Forest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ForestLevelUpdateView(GenericAPIView):
    pass
