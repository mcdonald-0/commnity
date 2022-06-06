from django.test import TestCase

from authentication.models import *


class FormsTestCase(TestCase):

    def test_login_user_with_wrong_password(self):
        User.objects.create_user(username='Mcdonald', password='password', email='mcdonald@mm.com')
        response = self.client.post('/signin/', {'email': 'mcdonald@mm.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)

    def test_login_user_with_an_email_that_does_not_exist(self):
        User.objects.create_user(username='Mcdonald', password='password', email='mcdonald@mm.com')
        response = self.client.post('/signin/', {'email': 'mcdonald2@mm.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)

