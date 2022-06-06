from django.test import TestCase


class UrlsTestCase(TestCase):

    def test_signup_url(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signin_url(self):
        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

        
