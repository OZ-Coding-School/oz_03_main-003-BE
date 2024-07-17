from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserGoogleTokenReceiverTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('google_receiver')  # Adjust the URL name as needed

    @patch('users.views.google_auth_view.requests.get')
    def test_google_auth_success(self, mock_get):
        # Mock Google API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "email": "testuser@gmail.com",
            "name": "Test User",
            "picture": "http://example.com/profile.jpg"
        }

        response = self.client.post(self.url, data={"access_token": "valid_access_token"}, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged in")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Verify the user is created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(email="testuser@gmail.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "Test User")
        self.assertEqual(user.profile_image, "http://example.com/profile.jpg")

    @patch('users.views.google_auth_view.requests.get')
    def test_google_auth_missing_token(self, mock_get):
        response = self.client.post(self.url, data={}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Failed to get user info")

    @patch('users.views.google_auth_view.requests.get')
    def test_google_auth_invalid_token(self, mock_get):
        # Mock Google API response for invalid token
        mock_get.return_value.status_code = 400

        response = self.client.post(self.url, data={"access_token": "invalid_access_token"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Failed to get user info")

    @patch('users.views.google_auth_view.requests.get')
    def test_existing_user_login(self, mock_get):
        # Create an existing user
        existing_user = User.objects.create(
            email="testuser@gmail.com",
            username="Existing User",
            profile_image="http://example.com/old_profile.jpg",
            last_login=timezone.now()
        )

        # Mock Google API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "email": "testuser@gmail.com",
            "name": "Test User",
            "picture": "http://example.com/profile.jpg"
        }

        response = self.client.post(self.url, data={"access_token": "valid_access_token"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged in")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Verify the user information is updated
        user = User.objects.get(email="testuser@gmail.com")
        self.assertEqual(user.username, "Existing User")  # Username should not change
        self.assertEqual(user.profile_image, "http://example.com/old_profile.jpg")  # Profile image should not change

    @patch('users.views.google_auth_view.requests.get')
    def test_google_auth_server_error(self, mock_get):
        # Simulate a server error from Google API
        mock_get.return_value.status_code = 500

        response = self.client.post(self.url, data={"access_token": "valid_access_token"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Failed to get user info")
