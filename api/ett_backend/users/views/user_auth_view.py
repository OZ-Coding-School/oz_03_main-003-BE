import os

from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken, TokenError

from users.serializers import (
    EmptySerializer,
    UserDeleteSerializer,
    UserLogoutSerializer,
    UserProfileSerializer,
    UserTokenRefreshSerializer,
)
from users.utils import EmotreeAuthClass


class UserTokenVerifyView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("access")
        if not token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            AccessToken(token)
            return Response(status=status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserTokenRefreshView(generics.GenericAPIView):
    serializer_class = UserTokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token not found in cookies"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"refresh_token": refresh_token})
        serializer.is_valid(raise_exception=True)

        try:
            access_token = EmotreeAuthClass.new_access_token_for_user(
                refresh_token=serializer.validated_data["refresh_token"]
            )
        except (InvalidToken, TokenError) as e:
            return Response(
                data={"error occurs": "UserTokenRefreshView", "detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(data={"access": access_token, "message": "Token refreshed successfully"})
        try:
            EmotreeAuthClass.set_cookie_attributes(response=response, key="access", token=access_token)
        except ValueError:
            return Response({"error occurs": "UserTokenRefreshView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={"refresh_token": request.COOKIES.get("refresh")})
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh_token"]
            with transaction.atomic():
                refresh_token.blacklist()
            response = Response(status=status.HTTP_200_OK)
            response.delete_cookie("access", domain=os.getenv("COOKIE_DOMAIN"), path="/")
            response.delete_cookie("refresh", domain=os.getenv("COOKIE_DOMAIN"), path="/")
            return response
        except (InvalidToken, TokenError) as e:
            return Response(
                data={"message": "Invalid refresh token", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDeleteView(generics.GenericAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        data = request.data.copy()
        data["refresh_token"] = request.COOKIES.get("refresh")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data["user"]
            refresh_token = serializer.validated_data["refresh_token"]
            with transaction.atomic():
                user.delete()
                refresh_token.blacklist()
            response = Response(status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie("access", domain=os.getenv("COOKIE_DOMAIN"), path="/")
            response.delete_cookie("refresh", domain=os.getenv("COOKIE_DOMAIN"), path="/")
            return response
        except (InvalidToken, TokenError) as e:
            return Response(
                data={"message": "Invalid refresh token", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
