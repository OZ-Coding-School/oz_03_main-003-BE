from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Forest
from trees.models import TreeMap
from .serializers import ForestSerializer


class ForestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_uuid):
        # Forest 생성 또는 조회 (CreateForest)
        forest, created = Forest.objects.get_or_create(user__uuid=user_uuid)
        serializer = ForestSerializer(forest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_forest_data(self, request, tree_uuid):
        # 특정 Forest 데이터 조회 (GetForestData)
        forest = Forest.objects.filter(trees__tree_map_uuid=tree_uuid).first()
        if forest:
            serializer = ForestSerializer(forest)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Forest를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        # Forest 삭제 (DeleteForest)
        data = request.data
        forest_uuid = data.get("forest_uuid")

        try:
            forest = Forest.objects.get(forest_uuid=forest_uuid)
            forest.delete()
            return Response({"detail": "Forest가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except Forest.DoesNotExist:
            return Response({"detail": "Forest를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
