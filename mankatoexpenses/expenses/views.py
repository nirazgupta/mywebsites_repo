from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template import Context
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(requests):
	return render(requests, 'expenses/index.html')

def edit(requests):
	return render(requests, 'expenses/edit.html')

def about(requests):
	return render(requests, 'expenses/about.html')

def transaction(requests):
	return render(requests, 'expenses/transaction.html')


# def login(requests):
# 	template_name = 'expenses/login.html'

# 	login(request, user)
# 	return render(requests, 'expenses/index.html')

class UserFormView(View):
	form_class = UserForm
	template_name = 'expenses/registration_form.html'
	
	# blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	# process reg_form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user.set_password(password)
			user.save()

			#authenticate user and login
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					request.user.username
					return redirect('index')

		return render(request, self.template_name, {'form':form})

	

# class LoginFormView(View):
# 	form_class = AuthenticationForm
# 	template_name = 'expenses/login.html'
	
# 	def get(self, request):
# 		form = self.form_class(None)
# 		return render(request, self.template_name, {'form':form})


# 	def post(self, request):
# 		form = self.form_class(request.POST)

# 		if form.is_valid():
# 			user = form.save(commit=False)
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password']

# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				if user.is_active:
# 					login(request,user)
# 					return redirect('index')
# 		return render(request, self.template_name, {'form':form})

def login_user(request):
	logout(request)
	username = ''
	password = ''

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('index')
	return render(request,'expenses/login.html')	


def logoutUser(request):
   logout(request)
   #return redirect('login.html')