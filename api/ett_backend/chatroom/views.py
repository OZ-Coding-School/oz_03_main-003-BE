import uuid

from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatroom.models import ChatRoom
from chatroom.serializers import ChatRoomCreateSerializer, ChatRoomSerializer, ChatRoomUpdateSerializer
from users.serializers import EmptySerializer


class ChatRoomCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomCreateSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            new_chatroom = ChatRoom.objects.create(
                user=user,
                chat_room_uuid=uuid.uuid4(),
                **serializer.validated_data,
            )
            new_chatroom.save()
        response_serializer = self.get_serializer(new_chatroom)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)


class ChatRoomListView(ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(user=self.request.user)


class ChatRoomRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "chat_room_uuid"

    def get(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get(self.lookup_field)
        chat_room = ChatRoom.objects.filter(chat_room_uuid=chat_room_uuid, user=request.user).first()
        if not chat_room:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChatRoomUpdateSerializer(instance=chat_room, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get(self.lookup_field)
        chat_room = ChatRoom.objects.filter(chat_room_uuid=chat_room_uuid, user=request.user).first()
        if not chat_room:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance=chat_room)
        return Response(status=status.HTTP_204_NO_CONTENT)
