from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import TokenError

from users.serializers import (
    UserDeleteSerializer,
    UserLogoutSerializer,
    UserTokenRefreshSerializer,
    UserProfileSerializer,
    EmptySerializer
)
from users.utils import generate_new_access_token_for_user, set_access_cookie


class UserTokenVerifyView(generics.GenericAPIView):
    serializer_class = TokenVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"detail": str(e)})


class UserTokenRefreshView(generics.GenericAPIView):
    serializer_class = UserTokenRefreshSerializer
    permission_classes = [AllowAny] # IsAuthenticated 클래스는 Access token을 사용하므로 AllowAny를 사용한다

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = request.data.get("refresh_token")
        access_token = generate_new_access_token_for_user(refresh_token=refresh_token)

        response= Response(data={"message": "Token refreshed successfully"})
        set_access_cookie(response=response, access_token=access_token)
        return response


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh_token"]
            with transaction.atomic():
                refresh_token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            return Response(
                data={"message": "Invalid refresh token", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDeleteView(generics.GenericAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data["user"]
            refresh_token = serializer.validated_data["refresh_token"]
            with transaction.atomic():
                user.delete()
                refresh_token.blacklist()
            return Response(data={"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except (InvalidToken, TokenError) as e:
            return Response(
                data={"message": "Invalid refresh token", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully updated user data"}, status=status.HTTP_200_OK)
