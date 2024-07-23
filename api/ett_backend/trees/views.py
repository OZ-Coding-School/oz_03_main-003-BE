from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from forest.models import Forest
from trees.models import TreeDetail, TreeEmotion
from trees.serializers import (
    FilteredTreeEmotionSerializer,
    TreeEmotionListSerializer,
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
        tree_uuid = request.query_params.get("tree_uuid")
        if tree_uuid:
            tree = get_object_or_404(TreeDetail.objects.select_related("forest"), tree_uuid=tree_uuid)
            serializer = self.get_serializer(tree)
            return Response(serializer.data, status=status.HTTP_200_OK)
        forest = get_object_or_404(Forest.objects.prefetch_related("related_tree"), user=user)
        serializer = self.get_serializer(forest.related_tree.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TreeUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = TreeUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "tree_uuid"
    queryset = TreeDetail.objects.all()

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
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance=tree)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TreeEmotionListView(ListAPIView):
    serializer_class = TreeEmotionListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        tree_uuid = request.query_params.get("tree_uuid")

        # tree_uuid를 제공한 경우
        if tree_uuid:
            tree_emotion = TreeEmotion.objects.select_related("tree").filter(tree__tree_uuid=tree_uuid).first()
            if not tree_emotion:
                return Response(data=[], status=status.HTTP_404_NOT_FOUND)

            if request.query_params.get("detail_sentiment"):
                serializer = FilteredTreeEmotionSerializer(tree_emotion, context={"request": request})
            else:
                serializer = self.get_serializer(data=tree_emotion)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # tree_uuid를 제공하지 않은 경우
        # User에 해당하고 Forest에 관련된 TreeDetail 객체를 역참조로 미리 가져온다. (쿼리 2개 발생)
        forest = Forest.objects.prefetch_related("related_tree").filter(user=user).first()
        if not forest:
            return Response(data=[], status=status.HTTP_404_NOT_FOUND)

        tree_details = forest.related_tree.all()  # 전체 tree 데이터를 가져온다
        if not tree_details.exists():
            # 쿼리에 해당하는 Tree가 전혀 존재하지 않다면
            return Response(data=[], status=status.HTTP_404_NOT_FOUND)

        # TreeDetail 객체에 해당하는 TreeEmotion 객체들을 가져온다
        tree_emotions = TreeEmotion.objects.filter(tree__in=tree_details).select_related("tree")
        if not tree_emotions.exists():
            # 해당 Tree에 감정 데이터가 존재하지 않는 경우
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.query_params.get("detail_sentiment"):  # detail_sentiment query_param이 존재하는 경우
            serializer = FilteredTreeEmotionSerializer(tree_emotions, many=True, context={"request": request})
        else:
            serializer = TreeEmotionListSerializer(tree_emotions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
