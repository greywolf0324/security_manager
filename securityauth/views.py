from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from . import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect


User = get_user_model()

# Create your views here.
# def signin(request):
#   if request.method == 'POST':
#     form = forms.SigninForm(request.POST)
#     if form.is_valid():
#       username = form.cleaned_data['email']
#       password = form.cleaned_data['password']
#       user = authenticate(request, username=username, password=password)
#       if user is not None:
#         print('user is found')
#         if user.is_allowed is False:
#           print('user is not allowed')
#           form.add_error(None, 'You are not allowed yet.')
#           return render(request, 'signin.html', { 'form': forms.SigninForm ,'is_signup_page': False})
#         login(request, user)
#         return redirect('security:home')  # Replace 'home' with the URL name of your home page
#       else:
#         print('user is not found')
#         form.add_error(None, 'Invalid username or password.')
#   else:
#      form = forms.SigninForm()
#   return render(request, 'signin.html', { 'form': forms.SigninForm,'is_signup_page': False })


def signin(request):
    if request.method == 'POST':
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_allowed is False:
                    return JsonResponse({'error_message': 'You are not allowed yet.'}, status=400)
                login(request, user)
                return JsonResponse({'redirect_url': reverse('security:home')})
            else:
                return JsonResponse({'error_message': 'Invalid username or password.'}, status=400)
        else:
            errors = {field: form.errors[field][0] for field in form.errors}
            return JsonResponse({'error_message': errors}, status=400)
    else:
        form = forms.SigninForm()
    return render(request, 'signin.html', {'form': forms.SigninForm, 'is_signup_page': False})

@csrf_protect
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