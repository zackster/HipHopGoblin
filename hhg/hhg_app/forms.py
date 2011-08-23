from django import forms
from django.forms import PasswordInput

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=30, label='Username', required=True)
	password = forms.CharField(label='Password',required=True, widget=PasswordInput())
	confirm = forms.CharField(label='Confirm Password',required=True, widget=PasswordInput())
	email = forms.EmailField(label='Email', required=True)
	#display = forms.CharField(label='Display Name',max_length=50)

class LoginForm(forms.Form):
        username = forms.CharField(max_length=30, label='Username', required=True)
        password = forms.CharField(label='Password',required=True, widget=PasswordInput())

class UploadForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()
        owned = forms.BooleanField(required=True, label="I own this file and agree to stream it")

