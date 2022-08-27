from django.db import models

from helpers.models import TrackingModel


class ReportedIssue(TrackingModel):
	title = models.CharField(max_length=200)
	reporter_ip_address = models.CharField(max_length=16)
	issue_in_detail = models.TextField(blank=True, null=True)
	date_reported = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{ self.title }'
