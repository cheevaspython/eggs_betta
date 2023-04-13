from django.test import TestCase


class ResponseTestCase(TestCase):

    def test_response(self):
        response = self.client.get('http://127.0.0.1:8000/api/swag/')
        self.assertEqual(response.status_code, 200)
