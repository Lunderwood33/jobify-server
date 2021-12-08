from django.db import models
from django.contrib.auth.models import User

class JobifyUser(models.Model):
    name = models.CharField(max_length=35)
    bio = models.CharField(max_length=50)
    isBusiness = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)