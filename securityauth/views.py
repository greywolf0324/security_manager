from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from . import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def signin(request):
  if request.method == 'POST':
    form = forms.SigninForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
      if user is not None:
        print('user is found')
        if user.is_allowed is False:
          print('user is not allowed')
          form.add_error(None, 'You are not allowed yet.')
          return render(request, 'signin.html', { 'form': forms.SigninForm ,'is_signup_page': False})
        login(request, user)
        return redirect('security:home')  # Replace 'home' with the URL name of your home page
      else:
        print('user is not found')
        form.add_error(None, 'Invalid username or password.')
  else:
     form = forms.SigninForm()
  return render(request, 'signin.html', { 'form': forms.SigninForm,'is_signup_page': False })

def signup(request):
  if request.method == 'POST':
    form = forms.SignupForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['email']
      password = form.cleaned_data['password']
      User.objects.create(username=username, email=username, password=make_password(password))
      return redirect('securityauth:signin')
    return render(request, 'signup.html', {'form': form, 'is_signup_page': True})    
  return render(request, 'signup.html', { 'form': forms.SignupForm, 'is_signup_page': True })