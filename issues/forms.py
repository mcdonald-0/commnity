from django import forms
from django.forms import ModelForm

from issues.models import ReportedIssue

class ReportAnIssueForm(ModelForm):
	title = forms.CharField(
		label="",
        widget=forms.TextInput(attrs={
        	'placeholder': 'Briefly describe the issue you encountered', 
        	'class': 'form-control'})
        )

	issue_in_detail = forms.CharField(
		label="",
		widget=forms.Textarea(attrs={
			'class': 'form-control', 
			'rows': 8, 
			'placeholder': 'Describe in detail the issue you found'
			})
		)
	class Meta:
		model = ReportedIssue
		fields = ['title', 'issue_in_detail']