from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch
from django.utils import timezone
from users.models import User

class UserGoogleTokenReceiverTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('google_receiver')

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

        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify Cookies are set
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)

        # Verify Cookie attributes
        access_cookie = response.cookies.get('access')
        refresh_cookie = response.cookies.get('refresh')

        if access_cookie:
            self.assertTrue(access_cookie['httponly'])
            self.assertEqual(access_cookie['samesite'], 'Lax')
            self.assertTrue(access_cookie['secure'])
            print('Access Cookie:')
            print('Value:', access_cookie.value)
            print('Expires:', access_cookie['expires'])
            print('Path:', access_cookie['path'])
            print('Domain:', access_cookie['domain'])
            print('Secure:', access_cookie['secure'])
            print('HttpOnly:', access_cookie['httponly'])
            print('SameSite:', access_cookie['samesite'])

        if refresh_cookie:
            self.assertTrue(refresh_cookie['httponly'])
            self.assertEqual(refresh_cookie['samesite'], 'Lax')
            self.assertTrue(refresh_cookie['secure'])
            print('Refresh Cookie:')
            print('Value:', refresh_cookie.value)
            print('Expires:', refresh_cookie['expires'])
            print('Path:', refresh_cookie['path'])
            print('Domain:', refresh_cookie['domain'])
            print('Secure:', refresh_cookie['secure'])
            print('HttpOnly:', refresh_cookie['httponly'])
            print('SameSite:', refresh_cookie['samesite'])

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
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)

        # Verify the user information is updated
        user = User.objects.get(email="testuser@gmail.com")
        self.assertEqual(user.username, "Existing User")
        self.assertEqual(user.profile_image, "http://example.com/old_profile.jpg")

    @patch('users.views.google_auth_view.requests.get')
    def test_google_auth_server_error(self, mock_get):
        # Simulate a server error from Google API
        mock_get.return_value.status_code = 500

        response = self.client.post(self.url, data={"access_token": "valid_access_token"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Failed to get user info")
