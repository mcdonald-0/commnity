from django.test import TestCase

from authentication.models import *
from users.models import *

class ViewsTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='Mcdonald', password='password', email='mcdonald@mm.com')

    # def test_get_user_profile(self):
    #     response = self.client.get('/user/1/')
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertTemplateUsed(response, 'view_profile.html')
    #     print(response)
        
    # def test_get_userprofile_that_does_not_exist(self):
    #     response = self.client.get('/user/2/')
    #     self.assertIs
    #     self.assertEqual(response.status_code, 200)
