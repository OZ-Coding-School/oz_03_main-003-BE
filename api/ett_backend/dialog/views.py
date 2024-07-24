import json

from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatroom.models import ChatRoom
from dialog.models import AIDialog, AIEmotionalAnalysis, UserDialog
from dialog.serializers import AIMessageSerializer, DialogSerializer, UserMessageSerializer
from gemini.models import GeminiModel


class UserMessageView(ListCreateAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get("chat_room_uuid")
        if not chat_room_uuid:
            return Response(data={"message": "chat_room_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)

        serializer = self.get_serializer(data=request.data)  # validate만 수행
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user_dialog = UserDialog.objects.create(
                user=request.user,
                chat_room=chat_room,
                message=serializer.validated_data["message"],
            )
            user_dialog.save()
        return Response(data={"message": "Successfully sent"}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get("chat_room_uuid")
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid, user=request.user)
        user_dialog = get_object_or_404(UserDialog, user=request.user, chat_room=chat_room)
        serializer = self.get_serializer(user_dialog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AIMessageView(RetrieveAPIView):
    serializer_class = AIMessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get("chat_room_uuid")
        chat_room = ChatRoom.objects.filter(user=request.user, chat_room_uuid=chat_room_uuid).first()
        user_dialog = UserDialog.objects.filter(user=request.user, chat_room=chat_room).first()

        model = GeminiModel().set_model()
        response = model.generate_content(str(user_dialog.message))

        # Gemini API 응답 데이터를 JSON 형식으로 파싱
        json_str = response._result.candidates[0].content.parts[0].text
        if not json_str:
            return Response(data={"message": "Failed to get response from AI"}, status=status.HTTP_404_NOT_FOUND)
        response_data = json.loads(json_str)

        # json 형식으로 응답 데이터 생성 (Django에서 전달하는)
        structured_response = {
            "sentiments": response_data.get("sentiments", {}),
            "message": response_data.get("message", ""),  # AI가 생성한 메세지.
        }

        # AIDialog instance 생성
        with transaction.atomic():
            ai_dialog = AIDialog.objects.create(
                user_dialog=user_dialog, message=structured_response["message"], applied_state=False
            )
            ai_dialog.save()

            ai_emotional_analysis = AIEmotionalAnalysis.objects.create(
                ai_dialog=ai_dialog,
                happiness=structured_response["sentiments"].get("happiness", 0.0),
                anger=structured_response["sentiments"].get("anger", 0.0),
                sadness=structured_response["sentiments"].get("sadness", 0.0),
                worry=structured_response["sentiments"].get("worry", 0.0),
                indifference=structured_response["sentiments"].get("indifference", 0.0),
            )
            ai_emotional_analysis.save()

        serializer = self.get_serializer(ai_dialog)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class DialogView(RetrieveAPIView):
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_room_uuid = kwargs.get("chat_room_uuid")
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid, user=request.user)

        user_dialog = get_object_or_404(UserDialog, user=request.user, chat_room=chat_room)
        ai_dialog = get_object_or_404(AIDialog, user_dialog=user_dialog)
        ai_emotional_analysis = get_object_or_404(AIEmotionalAnalysis, ai_dialog=ai_dialog)

        response_data = {
            "user": {"message_uuid": str(user_dialog.message_uuid), "message": user_dialog.message},
            "ai": {
                "message_uuid": str(ai_dialog.message_uuid),
                "message": ai_dialog.message,
                "sentiments": {
                    "happiness": ai_emotional_analysis.happiness,
                    "anger": ai_emotional_analysis.anger,
                    "sadness": ai_emotional_analysis.sadness,
                    "worry": ai_emotional_analysis.worry,
                    "indifference": ai_emotional_analysis.indifference,
                },
            },
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
