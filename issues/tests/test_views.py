from django.test import TestCase

from django.utils import timezone

from issues.models import *


class ViewsTestCase(TestCase):

	def test_get_reported_issue_view(self):
		response = self.client.get('/issues/report_an_issue/')
		self.assertEqual(response.status_code, 200)

	def test_create_a_reported_issue(self):
		response = self.client.post('/issues/report_an_issue/', {"title":"Issue reported", "reporter_ip_address":"192.168.43.110", "issue_in_detail":"well, this is the new ip address", "date_reported":"timezone.now()"})
		self.assertRedirects(response=response, expected_url='/', status_code=302, target_status_code=200)