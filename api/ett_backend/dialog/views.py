from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json

from dialog.models import UserDialog, AIDialog
from dialog.serializers import (
    UserDialogSerializer,
    AIDialogSerializer,
    UserMessageRetrieveSerializer,
    UserMessageListSerializer,
)
from gemini.models import GeminiModel


class UserMessagePostView(GenericAPIView):
    """
    User message post view
    """
    serializer_class = UserDialogSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # validation exception 발생하면 자동으로 에러코드 반환
        serializer.save()

        return Response(
            data={"message":"Successfully delivered message."},
            status=status.HTTP_201_CREATED
        )


class UserMessageRetrieveView(GenericAPIView):
    """
    User message retrieve view
    """
    serializer_class = UserMessageRetrieveSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response({
            "user_uuid": serializer.validated_data["user_uuid"],
            "chat_room_uuid": serializer.validated_data["chat_room_uuid"],
            "user_message": get_object_or_404(
                UserDialog, user=serializer.validated_data["user"],
                chat_room=serializer.validated_data["chat_room"]
            ).text
        })

class UserMessageListView(GenericAPIView):
    """
    Get all dialog list of User
    """
    serializer_class = UserMessageListSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user_dialog_queryset = UserDialog.objects.filter(
            user=serializer.validated_data["user"]
        )
        ai_dialog_queryset = AIDialog.objects.filter(
            user=serializer.validated_data["user"]
        )

        messages = []
        for user_dialog in user_dialog_queryset:
            ai_response = ai_dialog_queryset.filter(user_dialog=user_dialog).first()
            messages.append({
                "user_uuid": user_dialog.user.uuid,
                "chat_room_uuid": user_dialog.chat_room.chat_room_uuid,
                "user_message": user_dialog.text,
                "ai_response": ai_response.text if ai_response else None
            })

        return Response(messages, status=status.HTTP_200_OK)


class AIMessageRetrieveView(GenericAPIView):
    serializer_class = AIDialogSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        model = GeminiModel().set_model()
        response = model.generate_content(
            UserDialog.objects.filter(
                user=serializer.validated_data["user"],
                chat_room=serializer.validated_data["chat_room"]
            ).first().text
        )

        # Gemini API 응답 데이터를 JSON 형식으로 파싱
        response_data = json.loads(response)

        # json 형식으로 응답 데이터 생성 (Django에서 전달하는)
        structured_response = {
            "sentiments": response_data.get("sentiments", {}),
            "message": response_data.get("message", "") # AI가 생성한 메세지 입니다.
        }

        # AIDialog instance 생성
        AIDialog.objects.create(
            user=serializer.validated_data["user"],
            chat_room=serializer.validated_data["chat_room"],
            user_dialog=serializer.validated_data["user_dialog"],
            text=structured_response["message"],
        )

        return Response(
            data=structured_response,
            status=status.HTTP_200_OK,
        )
