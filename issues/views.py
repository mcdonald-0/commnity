from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect

from issues.models import *
from issues.forms import *

from helpers.views import *

def report_an_issue(request, *args, **kwargs):

	user_ip = get_client_ip(request)
	form = ReportAnIssueForm()

	if request.method == 'POST':
		form = ReportAnIssueForm(request.POST)
		if form.is_valid():
			issue_reported = ReportedIssue.objects.create(reporter_ip_address=user_ip, **form.cleaned_data)
			messages.success(request, "Thanks a lot for reporting an issue❣")
			messages.success(request, "We would do our best to attend to that; soonest😸")
		return redirect('questions:home')



	context = {
		'form': form
	}
	return render(request, 'issues/report.html', context)