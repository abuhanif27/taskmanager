from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignupForm

# Create your views here.


def login_view(request):
	if request.user.is_authenticated:
		return redirect(reverse('task_list'))

	form = LoginForm(request=request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		messages.success(request, 'Logged in successfully.')
		return redirect(reverse('task_list'))

	return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
	if request.method == 'POST':
		logout(request)
		messages.success(request, 'Logged out successfully.')
		return redirect(reverse('login'))

	return redirect(reverse('task_list'))


def signup_view(request):
	if request.user.is_authenticated:
		return redirect(reverse('task_list'))

	form = SignupForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.save()
		login(request, user)
		messages.success(request, 'Account created successfully. Welcome!')
		return redirect(reverse('task_list'))

	return render(request, 'accounts/signup.html', {'form': form})
