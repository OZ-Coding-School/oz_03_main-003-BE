from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dialog.models import AIDialog, AIEmotionalAnalysis
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
from users.utils import IsAdminUser


class TreeCreateView(CreateAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]
    MAX_TREE_COUNT = 9

    def create(self, request, *args, **kwargs):
        user = request.user

        forest = get_object_or_404(Forest, user=user)
        tree_count = TreeDetail.objects.filter(forest=forest).count()
        if tree_count >= self.MAX_TREE_COUNT:
            # 사용자의 현재 만들어진 트리의 개수가 9개 이상인 경우
            return Response(status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            new_tree = TreeDetail.objects.create(
                forest=forest,
                tree_name=f"My tree ({tree_count + 1})",
                location=tree_count,  # Tree 개수에 따라 현재 위치 결정
            )
            _ = TreeEmotion.objects.create(tree=new_tree)

        return Response(data={"tree_uuid": new_tree.tree_uuid}, status=status.HTTP_201_CREATED)


class TreeListView(ListAPIView):
    serializer_class = TreeSerializer
    permission_classes = [IsAuthenticated]
    queryset = TreeDetail.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        forest = get_object_or_404(Forest.objects.prefetch_related("related_tree"), user=user)
        serializer = self.get_serializer(forest.related_tree.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TreeListAdminView(ListAPIView):
    serializer_class = TreeSerializer
    permission_classes = [IsAdminUser]
    queryset = TreeDetail.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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


class TreeEmotionListAdminView(ListAPIView):
    serializer_class = TreeEmotionListSerializer
    permission_classes = [IsAdminUser]
    queryset = TreeEmotion.objects.all()

    def list(self, request, *args, **kwargs):
        # 만약 query param으로 detail_sentiment값이 들어왔다면
        if request.query_params.get("detail_sentiment"):
            serializer = FilteredTreeEmotionSerializer(self.get_queryset(), many=True, context={"request": request})
        else:
            serializer = TreeEmotionListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TreeEmotionRetrieveUpdateView(RetrieveUpdateAPIView):
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
        tree_uuid = kwargs.get(self.lookup_field)
        message_uuid = request.data.get("message_uuid")
        ai_dialog = get_object_or_404(AIDialog.objects.filter(message_uuid=message_uuid))

        # 해당 chat_room에 대해 이미 AI 응답이 Tree에 반영되었다면
        if ai_dialog.applied_state:
            return Response(data={"message": "Already applied"}, status=status.HTTP_400_BAD_REQUEST)

        ai_emotion_analysis = get_object_or_404(
            AIEmotionalAnalysis.objects.filter(ai_dialog__message_uuid=message_uuid)
        )

        # tree와 tree_emotion을 함께 찾아봄
        tree_emotion = (
            TreeEmotion.objects.select_related("tree")
            .filter(tree__tree_uuid=tree_uuid, tree__forest__user=request.user)
            .first()
        )
        if not tree_emotion:
            return Response(data={"message": "tree emotion not found"}, status=status.HTTP_404_NOT_FOUND)

        # serializer를 사용하여 데이터 업데이트
        emotion_data = {
            "happiness": ai_emotion_analysis.happiness,
            "sadness": ai_emotion_analysis.sadness,
            "anger": ai_emotion_analysis.anger,
            "worry": ai_emotion_analysis.worry,
            "indifference": ai_emotion_analysis.indifference,
        }
        serializer = TreeEmotionUpdateSerializer(instance=tree_emotion, data=emotion_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # ai_dialog의 상태 업데이트
        ai_dialog.applied_state = True
        ai_dialog.save()

        return Response(data={"message": "Successfully updated"}, status=status.HTTP_200_OK)
