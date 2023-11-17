from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()
class SigninForm(forms.Form):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
  email = forms.EmailField(required=True)
  password = forms.CharField(min_length=8, max_length=100, required=True, widget=forms.PasswordInput)

class SignupForm(forms.Form):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
  email = forms.EmailField(required=True)
  password = forms.CharField(min_length=8, max_length=100, required=True, widget=forms.PasswordInput)
  confirm_password = forms.CharField(min_length=8, max_length=100, required=True, widget=forms.PasswordInput)

  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError('This email is already in use.')
    return email