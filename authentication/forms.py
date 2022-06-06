from django import forms
from django.contrib.auth import authenticate

from django.utils.translation import gettext_lazy as _

from authentication.models import *

class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        label="", 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                }
            )
        )
    email = forms.CharField(
        label="", 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control', 
                }
            )
        )
    password = forms.CharField( 
        label='',
        min_length=6,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password', 
                'class': 'form-control',
                }
            )
        )
        #ToDo: I need to add password validators to the signup form.
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class SignInForm(forms.ModelForm):
    email = forms.EmailField(
        label="", 
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password', 
                'class': 'form-control',
                }
            )
        )
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            try:
                check_email = User.objects.get(email=email)
                if check_email:
                    raise forms.ValidationError(_(f'Incorrect password for email "{check_email}"😓'))

            except User.DoesNotExist:
                raise forms.ValidationError(_('You do not have an account yet😕, try creating one🙂!'))
           