from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User
import uuid

class AfterVerifyFailThenRefreshToken(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            uuid=uuid.uuid4().hex,
            social_platform="google",
            is_active=True,
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
        self.client.cookies['access'] = self.access_token
        self.client.cookies['refresh'] = self.refresh_token
        self.refresh_url = reverse('token_refresh')
        self.verify_url = reverse('token_verify')
        self.profile_url = reverse('user_profile')

    def test_verify_fail(self):
        # When: 1. 유효한 token으로 verify가 되는지 확인
        print("#" * 20)
        print("### 1.Access token: ", self.client.cookies['access'])
        print("### 1.Refresh token: ", self.client.cookies['refresh'])
        response = self.client.post(self.verify_url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # When: 2. Access token이 만료된 경우 verify 사용 시
        print("#" * 20)
        print("### 2. When access token expired")
        self.client.cookies['access'] = "invalid"
        response = self.client.post(self.verify_url)

        # Then: 401 에러 반환해야함
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # When: 3. 기존에 가지고 있는 Refresh token으로 새로운 access token 발급
        print("#" * 20)
        print("### 3. When refresh access token")
        print("### 3. refresh token: ", self.client.cookies['refresh'])
        response = self.client.post(self.refresh_url)

        # Then: payload에 uuid가 포함된 access token이 발급되어야함 (jwt.io)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        # When: 4. 재발급한 access token을 사용해서 사용자 정보를 가져오면
        print("#" * 20)
        print("### 4. Get user profile using refreshed access token")
        print("### 4. access token: ", self.client.cookies['access'])
        response = self.client.get(self.profile_url)

        # Then: 200 코드와 함께 사용자 정보를 가져온다
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
