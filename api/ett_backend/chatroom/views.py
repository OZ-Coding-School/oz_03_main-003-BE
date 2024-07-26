import uuid

from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatroom.models import ChatRoom
from chatroom.serializers import ChatRoomCreateSerializer, ChatRoomSerializer, ChatRoomUpdateSerializer
from trees.models import TreeDetail
from users.serializers import EmptySerializer
from users.utils import IsAdminUser


class ChatRoomCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomCreateSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tree = TreeDetail.objects.filter(tree_uuid=serializer.validated_data["tree_uuid"]).first()
        if not tree:
            return Response(data={"message": "tree not found"}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            new_chatroom = ChatRoom.objects.create(
                user=user,
                tree=tree,
                chat_room_uuid=uuid.uuid4(),
                chat_room_name=serializer.validated_data["chat_room_name"],
            )
            new_chatroom.save()
        response_serializer = self.get_serializer(new_chatroom)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)


class ChatRoomListView(ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        chat_rooms = ChatRoom.objects.filter(user=user)
        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChatRoomListForAdminView(ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAdminUser]
    queryset = ChatRoom.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChatRoomRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "chat_room_uuid"

    def get(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get(self.lookup_field)
        chat_room = ChatRoom.objects.filter(chat_room_uuid=chat_room_uuid, user=request.user).first()
        if not chat_room:
            return Response(data={"message": "chat room not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatRoomSerializer(chat_room)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        chat_room_uuid = kwargs.get(self.lookup_field)
        chat_room = ChatRoom.objects.filter(chat_room_uuid=chat_room_uuid, user=request.user).first()
        if not chat_room:
            return Response(data={"message": "chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatRoomUpdateSerializer(instance=chat_room, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data={"message": "Successfully updated"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get(self.lookup_field)
        chat_room = ChatRoom.objects.filter(chat_room_uuid=chat_room_uuid, user=request.user).first()
        if not chat_room:
            return Response(data={"message": "chat room not found"}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance=chat_room)
        return Response(status=status.HTTP_204_NO_CONTENT)
