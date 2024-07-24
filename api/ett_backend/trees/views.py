from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from trees.serializers import (
    FilteredTreeEmotionSerializer,
    TreeEmotionListSerializer,
    TreeEmotionSerializer,
    TreeEmotionUpdateSerializer,
    TreeSerializer,
    TreeUpdateSerializer,
)
from users.serializers import EmptySerializer


class TreeCreateView(CreateAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        forest = get_object_or_404(Forest, user=user)
        tree_count = TreeDetail.objects.filter(forest=forest).count()
        if tree_count >= 9:
            # 사용자의 현재 만들어진 트리의 개수가 9개 이상인 경우
            return Response(status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            new_tree = TreeDetail.objects.create(
                forest=forest,
                tree_name=f"My tree ({tree_count + 1})",
                location=tree_count,  # Tree 개수에 따라 현재 위치 결정
            )
            new_tree_emotion = TreeEmotion.objects.create(tree=new_tree)
            new_tree.save()
            new_tree_emotion.save()

        return Response(data={"tree_uuid": new_tree.tree_uuid}, status=status.HTTP_201_CREATED)


class TreeListView(ListAPIView):
    serializer_class = TreeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        forest = get_object_or_404(Forest.objects.prefetch_related("related_tree"), user=user)
        serializer = self.get_serializer(forest.related_tree.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TreeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TreeUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "tree_uuid"
    queryset = TreeDetail.objects.all()

    def get(self, request, *args, **kwargs):
        tree_uuid = kwargs.get(self.lookup_field)
        tree = get_object_or_404(TreeDetail.objects.select_related("forest"), tree_uuid=tree_uuid)
        serializer = TreeSerializer(tree)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        tree_uuid = kwargs.get(self.lookup_field)
        tree = TreeDetail.objects.filter(tree_uuid=tree_uuid, forest__user=request.user).first()
        if not tree:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=tree, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        tree_uuid = kwargs.get(self.lookup_field)
        tree = TreeDetail.objects.filter(tree_uuid=tree_uuid, forest__user=request.user).first()
        if not tree:
            return Response(data={"message": "tree not found"}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance=tree)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TreeEmotionListView(ListAPIView):
    serializer_class = TreeEmotionListSerializer
    permission_classes = [IsAuthenticated]
    queryset = TreeEmotion.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user

        # User가 소유한 Forest 데이터를 가져온다
        forest = get_object_or_404(Forest.objects.prefetch_related("related_tree"), user=user)
        tree_details = forest.related_tree.all()

        # Forest에 tree가 존재하지 않는 경우 -> json 응답으로 빈 배열 반환
        if not tree_details.exists():
            return Response(data=[], status=status.HTTP_200_OK)

        # TreeEmotion에서 정방향 참조하여 tree_details에 해당하는 데이터만 가져온다
        tree_emotions = TreeEmotion.objects.filter(tree__in=tree_details).select_related("tree")

        # 만약 query param으로 detail_sentiment값이 들어왔다면
        if request.query_params.get("detail_sentiment"):
            serializer = FilteredTreeEmotionSerializer(tree_emotions, many=True, context={"request": request})
        else:
            serializer = TreeEmotionListSerializer(tree_emotions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TreeEmotionRetrieveView(RetrieveUpdateAPIView):
    serializer_class = TreeEmotionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "tree_uuid"
    queryset = TreeEmotion.objects.all()

    def get(self, request, *args, **kwargs):
        tree_uuid = kwargs.get(self.lookup_field)
        tree_emotion = TreeEmotion.objects.select_related("tree").filter(tree__tree_uuid=tree_uuid).first()
        if not tree_emotion:
            return Response(data=[], status=status.HTTP_404_NOT_FOUND)

        if request.query_params.get("detail_sentiment"):
            serializer = FilteredTreeEmotionSerializer(tree_emotion, context={"request": request})
        else:
            serializer = self.get_serializer(tree_emotion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        tree_uuid = kwargs.get(self.lookup_field)
        tree = TreeDetail.objects.filter(tree_uuid=tree_uuid, forest__user=request.user).first()
        if not tree:
            return Response(data={"message": "tree not found"}, status=status.HTTP_404_NOT_FOUND)

        tree_emotion = TreeEmotion.objects.filter(tree=tree).first()
        if not tree_emotion:
            return Response(data={"message": "tree emotion not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TreeEmotionUpdateSerializer(instance=tree_emotion, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data={"message": "Successfully updated"}, status=status.HTTP_200_OK)
