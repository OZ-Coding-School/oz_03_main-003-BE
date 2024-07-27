from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import EmptySerializer, UserProfileSerializer, UserSerializer
from users.utils import IsAdminUser


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Successfully updated user data"}, status=status.HTTP_200_OK)


class UserUpdateAdminView(UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        pass


class UserViewForAdmin(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SwitchUserAuthorizationView(UpdateAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        is_superuser = request.data.get("is_superuser")
        if not is_superuser:
            return Response(data={"message": "is_superuser is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not (is_superuser == "True" or is_superuser == "False"):
            return Response(data={"message": "is_superuser must be True or False"}, status=status.HTTP_400_BAD_REQUEST)

        user_uuid = kwargs.get("user_uuid")
        user = get_object_or_404(User, uuid=user_uuid)
        if not user.is_active:
            return Response(data={"message": "User is not active"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_superuser = True if is_superuser == "True" else False
        user.save()
        return Response(status=status.HTTP_200_OK)
