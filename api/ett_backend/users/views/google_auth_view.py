import requests
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from users.models import User
from users.serializers import EmptySerializer, UserRegisterOrLoginSerializer
from users.utils import GoogleEnvironments, get_google_tokens_and_user_data, get_jwt_tokens_for_user


class UserGoogleLoginView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        env = GoogleEnvironments()
        redirect_uri = f"{env.main_domain}" + reverse("google_callback")
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={env.google_client_id}"
            f"&redirect_uri={redirect_uri}"
            "&scope=openid%20email%20profile"
            f"&state={env.google_state}"
        )
        if settings.TEST:
            return Response(
                data={"redirect_url": google_auth_url},
                status=status.HTTP_200_OK
            )
        return redirect(google_auth_url)


class UserGoogleLoginCallbackView(generics.GenericAPIView):
    serializer_class = UserRegisterOrLoginSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        env = GoogleEnvironments()
        authorization_code = request.GET.get("code")
        received_state = request.GET.get("state")

        # 구글서버에서 Callback이 호출되면 authorization code와 state를 넘겨주는데,
        # auth code는 access token을 발급하기 위한 것이며,
        # state는 CSRF 공격을 방지 용도이다.
        if not authorization_code:
            return Response({"message": "Authorization code is missing"}, status=status.HTTP_400_BAD_REQUEST)
        if received_state != env.google_state:
            return Response({"message": "State value does not match"}, status=status.HTTP_400_BAD_REQUEST)

        token_request_url = "https://oauth2.googleapis.com/token"
        token_params = {
            "grant_type": "authorization_code",
            "client_id": env.google_client_id,
            "client_secret": env.google_client_secret,
            "code": authorization_code,
            "redirect_uri": f"{env.main_domain}" + reverse("google_callback"),
        }

        # Google API를 이용하여 access token, id token을 가져온다.
        token_response = requests.post(token_request_url, data=token_params)
        if token_response.status_code != 200:
            return Response({"message": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        """
        id_token 안에는 jwt 형식으로 payload 내부에 사용자 정보가 들어있게 된다.
        # 이때 사용자 정보는, 기존에 Cloud Console에서 설정한 scope 범위로만 가져온다.
        {
            "access_token": jwt
            "expires_in": 3599,
            "scope":
            "token_type": "Bearer",
            "id_token": jwt
        }
        """
        token_data = token_response.json()
        if not token_data:
            return Response(data={"message": "Failed to get tokens and user info"}, status=status.HTTP_400_BAD_REQUEST)
        access_token, user_data = get_google_tokens_and_user_data(token_data)
        """
        user_data에 들어있는 정보는 아래와 같다.
        {
            "email":
            "name":
            "profile_image":
        }
        """

        serializer = self.get_serializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data["has_account"]:
            user = User.objects.create_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["name"],
                profile_image=serializer.validated_data["profile_image"],
                social_platform="google",
                last_login=timezone.now(),
            )
            user.save()
        else:
            user = serializer.validated_data["user"]
            user.last_login = timezone.now()
            user.save()

        # JWT 토큰 생성
        user_login_token = get_jwt_tokens_for_user(user)
        response = Response(
            data={
                "message": "Successfully logged in",
            },
            status=status.HTTP_200_OK,
        )

        # https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpResponse.set_cookie
        # JWT 토큰을 쿠키에 설정
        response.set_cookie(
            key="JWT_AUTH_ACCESS_COOKIE",
            value=user_login_token["access"],
            httponly=True,  # 클라이언트 측 스크립트에서 쿠키에 접근할 수 없도록 한다.
            secure=True,  # HTTPS를 통해서만 쿠키가 전송
            samesite="Lax",  # CSRF 공격 방지
            max_age=api_settings.ACCESS_TOKEN_LIFETIME.total_seconds(),  # 쿠키의 유효 기간 설정 (settings.py)
        )

        response.set_cookie(
            key="JWT_AUTH_REFRESH_COOKIE",
            value=user_login_token["refresh"],
            httponly=True,  # 클라이언트 측 스크립트에서 쿠키에 접근할 수 없도록 한다.
            secure=True,  # HTTPS를 통해서만 쿠키가 전송
            samesite="Lax",  # CSRF 공격 방지
            max_age=api_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),  # 쿠키의 유효 기간 설정 (settings.py)
        )

        return response
