from django.test import TestCase

from authentication.models import *


class ModelTestCase(TestCase):
    
    def test_create_user(self):
        user = User.objects.create_user(username='McDonald', password='Thisisthepassword', email='mcdonaldotoyo44@gmail.com', )
        self.assertEqual(user.username, 'McDonald')
    
    def test_create_superuser(self):
        user = User.objects.create_superuser(username='McDonald', password='Thisisthepassword', email='mcdonaldotoyo44@gmail.com', )
        self.assertEqual(user.username, 'McDonald')
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaisesMessage(ValueError, "Users must have an email address!"):
            User.objects.create_user(username='McDonald', password='Thisisthepassword', email='')
        
    def test_create_user_without_username(self):
        with self.assertRaisesMessage(ValueError, "Users must have a username!"):
            User.objects.create_user(username='', password='Thisisthepassword', email='mcdonaldotoyo44@gmail.com')
        
       