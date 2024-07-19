from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trees.models import TreeDetail

from .models import Forest, User
from .serializers import ForestSerializer


class ForestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        # Forest 생성 (CreateForest)
        data = request.data
        try:
            user = User.objects.get(uuid=uuid)
            forest = Forest.objects.create(user=user, **data)
            serializer = ForestSerializer(forest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)


class ForestRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        # 사용자의 Forest 조회 (RetrieveForest)
        try:
            forest = Forest.objects.get(user__uuid=uuid)
            serializer = ForestSerializer(forest)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Forest.DoesNotExist:
            return Response({"message": "Forest Not Found"}, status=status.HTTP_404_NOT_FOUND)


class ForestDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # Forest 삭제 (DeleteForest)
        data = request.data
        forest_uuid = data.get("forest_uuid")

        try:
            forest = Forest.objects.get(forest_uuid=forest_uuid)
            forest.delete()
            return Response({"message": "Successfully Deleted Forest"}, status=status.HTTP_204_NO_CONTENT)
        except Forest.DoesNotExist:
            return Response({"message": "Forest not found"}, status=status.HTTP_404_NOT_FOUND)
