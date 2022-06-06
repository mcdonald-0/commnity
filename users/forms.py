from django.contrib.admin.widgets import AdminDateWidget
from django import forms

from users.models import *


class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(
    max_length=150, 
    label="", 
    widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            }
        )
    )

    last_name = forms.CharField(
    max_length=150, 
    label="", 
    widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            }
        )
    )

    GENDER_CHOICES = (
    		('M', 'Male'),
    		('F', 'Female'),
     	)
    gender = forms.CharField(
        max_length=1,
        widget=forms.RadioSelect(
            choices=GENDER_CHOICES,
        )
    )

    birthdate = forms.DateField(widget=forms.SelectDateWidget)

    bio = forms.CharField(
		label="",
		widget=forms.Textarea(attrs={
			'class': 'form-control', 
			'rows': 3, 
			'placeholder': 'You can write a little about yourself...'
			})
		)

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user',]
        
    
    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        profile.profile_image = self.cleaned_data['profile_image']
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']
        profile.birthdate = self.cleaned_data['birthdate']
        profile.gender = self.cleaned_data['gender']
        profile.bio = self.cleaned_data['bio']
        profile.date_of_profile_update = timezone.now()
        if commit:
            profile.save()
            return profile

# TOdo: i need to download an edit profile template so it kinda goes well with this



        