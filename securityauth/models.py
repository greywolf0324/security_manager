from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  is_allowed = models.BooleanField(default=False)
# Create your models here.
