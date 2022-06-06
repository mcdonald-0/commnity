from django import forms
from django.forms import ModelForm

from questions.models import Answer, Question


class AnswerForm(ModelForm):
	answer = forms.CharField(
		widget=forms.Textarea(attrs={
			'class': 'form-control', 
			'cols': 8,
			'rows': 8, 
			'placeholder': 'Do you have an answer🤔 leave a comment!'
			})
		)
	class Meta:
		model = Answer
		fields = ['answer']


class AskQuestionForm(ModelForm):
	title = forms.CharField(
		label="",
        widget=forms.TextInput(attrs={
        	'placeholder': 'What\'s your question title', 
        	'class': 'form-control'})
        )  
	
	question = forms.CharField(
		label="",
		widget=forms.Textarea(attrs={
			'class': 'form-control', 
			'rows': 8, 
			'placeholder': 'Your full question goes here!'
			})
		)

	class Meta:
		model = Question
		fields = ['title', 'question']
