from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.logger import logger
from users.models import User
from users.serializers import EmptySerializer, UserProfileSerializer, UserSerializer
from users.utils import IsAdminUser


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/user/profile")
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        if partial:
            logger.info("PATCH /api/user/profile")
        else:
            logger.info("PUT /api/user/profile")

        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Successfully updated user data"}, status=status.HTTP_200_OK)


class UserRetrieveUpdateDeleteAdminView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "user_uuid"
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        logger.info(f"GET /api/user/{kwargs.get(self.lookup_field)}")
        user_uuid = kwargs.get(self.lookup_field)
        user = get_object_or_404(User, uuid=user_uuid)
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        if partial:
            logger.info(f"PATCH /api/user/{kwargs.get(self.lookup_field)}")
        else:
            logger.info(f"PUT /api/user/{kwargs.get(self.lookup_field)}")

        user_uuid = kwargs.get(self.lookup_field)
        user = get_object_or_404(User, uuid=user_uuid)
        serializer = UserProfileSerializer(instance=user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Successfully updated user data"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"DELETE /api/user/{kwargs.get(self.lookup_field)}")
        user_uuid = kwargs.get(self.lookup_field)
        user = get_object_or_404(User, uuid=user_uuid)
        self.perform_destroy(instance=user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListForAdmin(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        logger.info("GET /api/user")
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SwitchUserAuthorizationView(UpdateAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        logger.info("PUT /api/user/state/<uuid:user_uuid>")
        is_superuser = request.data.get("is_superuser")
        if not is_superuser:
            logger.error("PUT /api/user/state/<uuid:user_uuid>: is_superuser is required")
            return Response(data={"message": "is_superuser is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not (is_superuser == "True" or is_superuser == "False"):
            logger.error("PUT /api/user/state/<uuid:user_uuid>: is_superuser must be True or False with String type")
            return Response(data={"message": "is_superuser must be True or False"}, status=status.HTTP_400_BAD_REQUEST)

        user_uuid = kwargs.get("user_uuid")
        user = get_object_or_404(User, uuid=user_uuid)
        if not user.is_active:
            logger.error("PUT /api/user/state/<uuid:user_uuid>: User is not active")
            return Response(data={"message": "User is not active"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_superuser = True if is_superuser == "True" else False
        user.save()
        return Response(status=status.HTTP_200_OK)
