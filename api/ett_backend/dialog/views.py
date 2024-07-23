import json

from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatroom.models import ChatRoom
from dialog.models import AIDialog, UserDialog
from dialog.serializers import UserMessageSerializer
from gemini.models import GeminiModel
from users.serializers import EmptySerializer


class UserMessageCreateView(CreateAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user_dialog = UserDialog.objects.create(
                user=request.user,
                chat_room=serializer.validated_data["chat_room"],
                text=serializer.validated_data["message"],
            )
            user_dialog.save()
        return Response(status=status.HTTP_201_CREATED)


# class UserMessageRetrieveView(GenericAPIView):
#     """
#     User message retrieve view
#     """
#
#     serializer_class = UserMessageRetrieveSerializer
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(
#             {
#                 "user_uuid": serializer.validated_data["user_uuid"],
#                 "chat_room_uuid": serializer.validated_data["chat_room_uuid"],
#                 "user_message": get_object_or_404(
#                     UserDialog, user=serializer.validated_data["user"], chat_room=serializer.validated_data["chat_room"]
#                 ).text,
#             }
#         )


# class UserMessageListView(GenericAPIView):
#     """
#     Get all dialog list of User
#     """
#
#     serializer_class = UserMessageListSerializer
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         user_dialog_queryset = UserDialog.objects.filter(user=serializer.validated_data["user"])
#         ai_dialog_queryset = AIDialog.objects.filter(user=serializer.validated_data["user"])
#
#         messages = []
#         for user_dialog in user_dialog_queryset:
#             ai_response = ai_dialog_queryset.filter(user_dialog=user_dialog).first()
#             messages.append(
#                 {
#                     "user_uuid": user_dialog.user.uuid,
#                     "chat_room_uuid": user_dialog.chat_room.chat_room_uuid,
#                     "user_message": user_dialog.text,
#                     "ai_response": ai_response.text if ai_response else None,
#                 }
#             )
#
#         return Response(messages, status=status.HTTP_200_OK)


class AIMessageRetrieveView(RetrieveAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        chat_room_uuid = kwargs.get("chat_room_uuid")
        chat_room = ChatRoom.objects.filter(user=user, chat_room_uuid=chat_room_uuid).first()
        user_dialog = UserDialog.objects.filter(user=user, chat_room=chat_room).first()

        model = GeminiModel().set_model()
        response = model.generate_content(user_dialog.message)

        # Gemini API 응답 데이터를 JSON 형식으로 파싱
        response_data = json.loads(response)

        # json 형식으로 응답 데이터 생성 (Django에서 전달하는)
        structured_response = {
            "sentiments": response_data.get("sentiments", {}),
            "message": response_data.get("message", ""),  # AI가 생성한 메세지.
        }

        # AIDialog instance 생성
        with transaction.atomic():
            AIDialog.objects.create(
                user_dialog=user_dialog,
                message=structured_response["message"],
                sentiments=structured_response["sentiments"],
            )

        return Response(
            data=structured_response,
            status=status.HTTP_200_OK,
        )
