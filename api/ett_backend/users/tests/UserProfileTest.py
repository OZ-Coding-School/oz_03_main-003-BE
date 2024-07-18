from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from io import BytesIO
from PIL import Image
from users.models import User

class UserProfileTest(APITestCase):

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
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.url = reverse("user_profile")

    def test_get_user_profile(self):
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Successfully updated user data")

        # 확인: 사용자 정보가 업데이트되었는지 확인
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updateduser@example.com")

    def test_update_user_profile_with_image(self):
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, 'jpeg')
        image.seek(0)
        image_file = SimpleUploadedFile("profile_image.jpg", image.getvalue(), content_type="image/jpeg")

        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "profile_image": image_file,
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Successfully updated user data")

        # 프로필 이미지가 업데이트되었는지 확인
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updateduser@example.com")
        self.assertTrue(self.user.profile_image.startswith("https://"))
        print(self.user)
