from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json

from .models import ChatRoom, UserDialog, AIDialog
from users.models import User
from .serializers import UserDialogSerializer
from gemini.models import GeminiModel

class UserMessagePostView(GenericAPIView):
    """
    User message post view
    """
    serializer_class = UserDialogSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_uuid = request.query_params.get('user_uuid')
        chat_room_uuid = request.query_params.get('chat_room_uuid')
        user_message = request.data.get('message')

        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)
        if not chat_room:
            return Response(
                data={"message": "Invalid Chat Room UUID."},
                status=status.HTTP_404_NOT_FOUND
            )

        user = get_object_or_404(User, uuid=user_uuid)
        if not user:
            return Response(
                data={"message": "Invalid User UUID."},
                status=status.HTTP_404_NOT_FOUND
            )

        UserDialog.objects.create(
            user=user,
            chat_room=chat_room,
            text=user_message
        )

        # TODO: Send message to AI Async with Celery
        # send_message_to_ai(user_uuid, chat_room_uuid, user_message)

        return Response(
            data={"message":"Successfully delivered message."},
            status=status.HTTP_201_CREATED
        )


class AIMessageRetrieveView(GenericAPIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = GeminiModel().set_model()

    def get(self, request, *args, **kwargs):
        user_uuid = request.query_params.get('user_uuid')
        chat_room_uuid = request.query_params.get('chat_room_uuid')
        user_message = request.query_params.get('message')

        if not user_uuid:
            return Response(
                data={"message": "User UUID is not given"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not chat_room_uuid:
            return Response(
                data={"message": "Chat Room UUID is not given"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user_message:
            return Response(
                data={"message": "User message is not given"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = self.model.generate_content(user_message)

        # 응답 데이터를 JSON 형식으로 파싱
        response_data = json.loads(response)

        # 구조화된 응답 데이터 생성
        structured_response = {
            "sentiments": response_data.get("sentiments", {}),
            "message": response_data.get("message", "")
        }

        user = get_object_or_404(User, uuid=user_uuid)
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)
        user_dialog = UserDialog.objects.filter(
            Q(user=user) & Q(chat_room=chat_room)
        ).first()

        AIDialog.objects.create(
            user=user,
            chat_room=chat_room,
            user_dialog=user_dialog,
            text=response_data.get("message", "")
        )

        return Response(
            data=structured_response,
            status=status.HTTP_200_OK,
        )
