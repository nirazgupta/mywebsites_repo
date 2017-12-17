from django import forms
from django.contrib.auth.models import User

# class TranForm(forms.Form):
# 	"""docstring for TranForm"""
# 	Date = forms.DateInput(attrs={'class':'datepicker'})
	
class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username',  'password', 'email']

# class LoginForm(forms.ModelForm):
# 	password = forms.CharField(widget = forms.PasswordInput)

# 	class Meta:
# 		model = User
# 		fields = ['username',  'password']