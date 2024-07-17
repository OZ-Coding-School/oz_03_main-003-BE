from django.test import TestCase


class HealthCheck(TestCase):

    def test_health_check_api(self):
        response = self.client.get(path="/api/health/")

        if response.status_code == 200:
            self.assertEqual(response.data, "OK")
