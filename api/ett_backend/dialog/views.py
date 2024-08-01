import json

from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatroom.models import ChatRoom
from common.logger import logger
from dialog.models import AIDialog, AIEmotionalAnalysis, UserDialog
from dialog.serializers import AIMessageSerializer, DialogSerializer, UserMessageSerializer
from gemini.models import GeminiModel


class UserMessageView(ListCreateAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        logger.info("POST /api/message/user/<uuid:chat_room_uuid>")
        chat_room_uuid = kwargs.get("chat_room_uuid")
        if not chat_room_uuid:
            logger.error("/api/message/user/<uuid:chat_room_uuid>: chat_room_uuid is required")
            return Response(data={"message": "chat_room_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)
        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid)

        serializer = self.get_serializer(data=request.data)  # validate만 수행
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user_dialog = UserDialog.objects.create(
                user=request.user, chat_room=chat_room, message=serializer.validated_data["message"]
            )
            user_dialog.save()
        return Response(data={"message_uuid": str(user_dialog.message_uuid)}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/message/user/<uuid:chat_room_uuid>")
        chat_room_uuid = kwargs.get("chat_room_uuid")
        if not chat_room_uuid:
            logger.error("/api/message/user/<uuid:chat_room_uuid>: chat_room_uuid is required")
            return Response(data={"message": "chat_room_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_dialog = UserDialog.objects.filter(
            chat_room__chat_room_uuid=chat_room_uuid, chat_room__user=request.user, user=request.user
        )
        if not user_dialog:
            logger.error("/api/message/user/<uuid:chat_room_uuid>: user dialog not found")
            return Response(data={"message": "user dialog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user_dialog, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AIMessageView(ListCreateAPIView):
    serializer_class = AIMessageSerializer
    permission_classes = [IsAuthenticated]

    INDIFFERENCE_WEIGHT = 0.6

    def create(self, request, *args, **kwargs):
        logger.info("POST /api/message/ai/<uuid:chat_room_uuid>")
        chat_room_uuid = kwargs.get("chat_room_uuid")
        if not chat_room_uuid:
            logger.error("/api/message/ai/<uuid:chat_room_uuid>: chat_room_uuid is required")
            return Response(data={"message": "chat_room_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)

        message_uuid = request.data.get("message_uuid")
        if not message_uuid:
            logger.error("/api/message/ai/<uuid:chat_room_uuid>: message_uuid is required")
            return Response(data={"message": "message_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_dialog = UserDialog.objects.get(
                chat_room__chat_room_uuid=chat_room_uuid, message_uuid=message_uuid, user=request.user
            )
        except UserDialog.DoesNotExist:
            logger.error("/api/message/ai/<uuid:chat_room_uuid>: user dialog not found")
            return Response(data={"message": "user dialog not found"}, status=status.HTTP_404_NOT_FOUND)

        model = GeminiModel().set_model()
        response = model.generate_content(str(user_dialog.message))

        # Gemini API 응답 데이터를 JSON 형식으로 파싱
        json_str = response._result.candidates[0].content.parts[0].text
        if not json_str:
            logger.error("/api/message/ai/<uuid:chat_room_uuid>: Failed to get response from AI")
            return Response(data={"message": "Failed to get response from AI"}, status=status.HTTP_404_NOT_FOUND)
        response_data = json.loads(json_str)

        # json 형식으로 응답 데이터 생성 (Django에서 전달하는)
        structured_response = {
            "sentiments": response_data.get("sentiments", {}),
            "message": response_data.get("message", ""),  # AI가 생성한 메세지.
        }

        # AIDialog instance 생성
        with transaction.atomic():
            ai_dialog, created = AIDialog.objects.update_or_create(
                user_dialog=user_dialog, defaults={"message": structured_response["message"], "applied_state": False}
            )
            AIEmotionalAnalysis.objects.update_or_create(
                ai_dialog=ai_dialog,
                defaults={
                    "happiness": structured_response["sentiments"].get("happiness", 0.0),
                    "anger": structured_response["sentiments"].get("anger", 0.0),
                    "sadness": structured_response["sentiments"].get("sadness", 0.0),
                    "worry": structured_response["sentiments"].get("worry", 0.0),
                    "indifference":
                        round(structured_response["sentiments"].get("indifference", 0.0) * self.INDIFFERENCE_WEIGHT, 1),
                },
            )

        serializer = self.get_serializer(ai_dialog)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/message/ai/<uuid:chat_room_uuid>")
        chat_room_uuid = kwargs.get("chat_room_uuid")
        if not chat_room_uuid:
            logger.error("/api/message/ai/<uuid:chat_room_uuid>: chat_room_uuid is required")
            return Response(data={"message": "chat_room_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)

        ai_dialog = AIDialog.objects.filter(
            user_dialog__user=request.user,
            user_dialog__chat_room__chat_room_uuid=chat_room_uuid,
        )
        if not ai_dialog:
            logger.error("/api/message/ai/<uuid:chat_room_uuid>: ai dialog not found")
            return Response(data={"message": "ai dialog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(ai_dialog, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DialogListView(RetrieveAPIView):
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/dialog/<uuid:chat_room_uuid>")
        chat_room_uuid = kwargs.get("chat_room_uuid")
        if not chat_room_uuid:
            logger.error("/api/dialog/<uuid:chat_room_uuid>: chat_room_uuid is required")
            return Response(data={"message": "chat_room_uuid is required"}, status=status.HTTP_400_BAD_REQUEST)

        chat_room = get_object_or_404(ChatRoom, chat_room_uuid=chat_room_uuid, user=request.user)
        user_dialogs = UserDialog.objects.filter(chat_room=chat_room).select_related("ai_dialog").order_by("created_at")
        response_data = []

        for user_dialog in user_dialogs:
            ai_dialog = AIDialog.objects.filter(user_dialog=user_dialog).first()
            if ai_dialog:
                ai_emotional_analysis = AIEmotionalAnalysis.objects.filter(ai_dialog=ai_dialog).first()
                if ai_emotional_analysis:
                    response_data.append(
                        {
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
                            "applied_state": ai_dialog.applied_state,
                        }
                    )
                else:
                    response_data.append(
                        {
                            "user": {"message_uuid": str(user_dialog.message_uuid), "message": user_dialog.message},
                            "ai": {
                                "message_uuid": str(ai_dialog.message_uuid),
                                "message": ai_dialog.message,
                                "sentiments": {},
                            },
                        }
                    )
            else:
                response_data.append(
                    {
                        "user": {"message_uuid": str(user_dialog.message_uuid), "message": user_dialog.message},
                        "ai": {},
                    }
                )

        return Response(data=response_data, status=status.HTTP_200_OK)
