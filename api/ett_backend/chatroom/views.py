from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from chatroom.serializers import ChatRoomCreateSerializer, ChatRoomListSerializer, ChatRoomRetrieveSerializer, \
    ChatRoomUpdateSerializer, ChatRoomDeleteSerializer
from chatroom.models import ChatRoom
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class ChatRoomCreateView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ChatRoomCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "chat_room_uuid": serializer.validated_data["chat_room_uuid"]
            },
            status=status.HTTP_201_CREATED
        )


class ChatRoomListView(GenericAPIView):
    serializer_class = ChatRoomListSerializer
    permission_classes = [AllowAny]
    queryset = ChatRoom.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        chat_room_queryset = ChatRoom.objects.filter(
            user=serializer.validated_data["user"]
        )

        chat_rooms = []
        for chat_room in chat_room_queryset:
            chat_rooms.append(
                {
                    "chat_room_uuid": chat_room.chat_room_uuid,
                    "chat_room_name": chat_room.chat_room_name
                }
            )

        return Response(
            data=chat_rooms,
            status=status.HTTP_200_OK
        )


class ChatRoomRetrieveView(GenericAPIView):
    serializer_class = ChatRoomRetrieveSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={
                "chat_room_uuid": serializer.validated_data["chat_room_uuid"],
                "chat_room_name": serializer.validated_data["chat_room_name"],
                "analyze_target_name": serializer.validated_data["analyze_target_name"],
                "analyze_target_relation": serializer.validated_data["analyze_target_relation"],
            },
            status=status.HTTP_200_OK
        )

class ChatRoomUpdateView(UpdateAPIView):
    serializer_class = ChatRoomUpdateSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat_room = serializer.validated_data["chat_room"]
        serializer.update(chat_room, serializer.validated_data)

        return Response(
            data={
                "message": "Successfully updated chat room.",
                "chat_room_uuid": chat_room.chat_room_uuid,
            },
            status=status.HTTP_200_OK
        )

class ChatRoomDeleteView(DestroyAPIView):
    serializer_class = ChatRoomDeleteSerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        chat_room = serializer.validated_data["chat_room"]
        chat_room.delete()

        return Response(
            data={
                "message": "Successfully deleted chat room.",
            },
            status=status.HTTP_204_NO_CONTENT
        )
