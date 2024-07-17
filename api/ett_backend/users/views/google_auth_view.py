import requests
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import EmptySerializer
from users.utils import get_jwt_tokens_for_user
from rest_framework.response import Response
from rest_framework import status

class UserGoogleTokenReceiver(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"message": "Access token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Google API를 통해 사용자 정보 가져오기
        userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        userinfo_response = requests.get(userinfo_url, headers={'Authorization': f"Bearer {access_token}"})

        if userinfo_response.status_code != 200:
            return Response({"message": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)

        userinfo = userinfo_response.json()

        # 사용자 정보 저장 또는 업데이트
        email = userinfo.get("email")
        name = userinfo.get("name")
        profile_image = userinfo.get("picture")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": name,
                "profile_image": profile_image,
                "social_platform": "google",
            }
        )

        if not created:
            user.last_login = timezone.now()
            user.save()

        # JWT 토큰 생성
        jwt_tokens = get_jwt_tokens_for_user(user)

        return Response(
            data = {
                "message": "Successfully logged in",
                "access": jwt_tokens['access'],
                "refresh": jwt_tokens['refresh']
            },
            status=status.HTTP_200_OK
        )
