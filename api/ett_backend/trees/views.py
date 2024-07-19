from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TreeDetail

# from .serializers import TreeDetailSerializer, TreeMapSerializer


class TreeManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 트리 맵 조회
        try:
            tree_map = TreeMap.objects.get(user=request.user)
            # serializer = TreeMapSerializer(tree_map)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TreeMap.DoesNotExist:
            return Response({"detail": "TreeMap을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        # 트리 이름 변경
        try:
            tree_map = TreeMap.objects.get(user=request.user)
            data = request.data
            tree_name = data.get("tree_name")

            tree_detail = TreeDetail.objects.get(tree_map=tree_map)
            tree_detail.tree_name = tree_name
            tree_detail.save()

            # serializer = TreeDetailSerializer(tree_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TreeMap.DoesNotExist:
            return Response({"detail": "TreeMap을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except TreeDetail.DoesNotExist:
            return Response({"detail": "TreeDetail을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        # 트리 삭제
        try:
            tree_map = TreeMap.objects.get(user=request.user)
            tree_map.delete()
            return Response({"detail": "트리가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except TreeMap.DoesNotExist:
            return Response({"detail": "TreeMap을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def get_all_tree_names(self, request):
        # 전체 나무 이름 데이터 조회
        tree_details = TreeDetail.objects.all()
        # serializer = TreeDetailSerializer(tree_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_emotion_data(self, request):
        # 감정 데이터 총합 조회
        try:
            tree_map = TreeMap.objects.get(user=request.user)
            tree_details = TreeDetail.objects.filter(tree_map=tree_map)

            total_happiness = sum(tree.happiness for tree in tree_details)
            total_anger = sum(tree.anger for tree in tree_details)
            total_sadness = sum(tree.sadness for tree in tree_details)
            total_worry = sum(tree.worry for tree in tree_details)

            return Response(
                {
                    "total_happiness": total_happiness,
                    "total_anger": total_anger,
                    "total_sadness": total_sadness,
                    "total_worry": total_worry,
                },
                status=status.HTTP_200_OK,
            )
        except TreeMap.DoesNotExist:
            return Response({"detail": "TreeMap을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
