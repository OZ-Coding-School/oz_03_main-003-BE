from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AIDialog, ChatRoom, UserDialog
from .serializers import AIDialogSerializer, ChatRoomSerializer, UserDialogSerializer


class ChatRoomListCreateView(APIView):
    # GET : 채팅방 목록 불러오기
    def get(self, request):
        chat_rooms = ChatRoom.objects.all()
        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data)

    # POST : 새로운 채팅방 생성
    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            chat_room = serializer.save()
            return Response(ChatRoomSerializer(chat_room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomDetailView(APIView):
    # GET : 특정 채팅방 가져오기
    def get(self, request, chat_room_uuid):
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)
        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data)

    # DELETE : 해당 채팅방 삭제
    def delete(self, request, chat_room_uuid):
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)
        chat_room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDialogListCreateView(APIView):
    # GET : 특정 채팅방 정보 조회
    def get(self, request, chat_room_uuid):
        user_dialogs = UserDialog.objects.filter(chat_room__chat_room_uuid=chat_room_uuid)
        serializer = UserDialogSerializer(user_dialogs, many=True)
        return Response(serializer.data)

    # POST : 메시지 전송
    def post(self, request, chat_room_uuid):
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)
        serializer = UserDialogSerializer(data=request.data)
        if serializer.is_valid():
            user_dialog = serializer.save(chat_room=chat_room)
            return Response(UserDialogSerializer(user_dialog).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIDialogListView(APIView):
    # GET : AI로부터 받은 메시지 조회
    def get(self, request, chat_room_uuid):
        ai_dialogs = AIDialog.objects.filter(user_dialog__chat_room__chat_room_uuid=chat_room_uuid)
        serializer = AIDialogSerializer(ai_dialogs, many=True)
        return Response(serializer.data)
