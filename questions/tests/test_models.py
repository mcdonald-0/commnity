from django.test import TestCase

from questions.models import *
from authentication.models import *
from users.models import *

class ModelsTestCase(TestCase):

	def setUp(self):
		user = User.objects.create_user(username='McDonald', password='Thisisthepassword', email='mcdonaldotoyo44@gmail.com', )
		user_profile = UserProfile.objects.create(
			user = user,
			profile_image
			first_name
			last_name
			birthdate
			gender
			bio
			date_of_profile_update		
		)


	def test_create_question(self):
