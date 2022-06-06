from django.test import TestCase

from django.utils import timezone

from issues.models import *


class ModelTestCase(TestCase):

    def setUp(self):
        ReportedIssue.objects.create(
            title = "Issue reported",
            reporter_ip_address = "192.168.43.110",
            issue_in_detail = "well, this is the new ip address",
            date_reported = timezone.now(),
            )

    def test_get_created_reported_issue(self):
        item = ReportedIssue.objects.get(pk=1)
        self.assertEqual(item.title, "Issue reported")

    
   