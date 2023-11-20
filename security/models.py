from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class ProcessHistory(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  input = models.CharField(max_length=255, null=True)
  output = models.CharField(max_length=255, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  