from django.test import TestCase

from authentication.models import *


class ViewsTestCase(TestCase):

    def test_user_signup(self):
        response = self.client.post('/signup/', {'username': 'Mcdonald', 'password': 'password', 'email': 'mcdonald@mm.com'})
        self.assertRedirects(response=response, expected_url='/signin/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 302)

    def test_user_signin(self):
        User.objects.create_user(username='Mcdonald', password='password', email='mcdonald@mm.com')
        response = self.client.post('/signin/', {'email': 'mcdonald@mm.com', 'password': 'password'})
        self.assertRedirects(response=response, expected_url='/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 302)


