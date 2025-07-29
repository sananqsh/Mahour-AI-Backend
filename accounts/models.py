from django.contrib.auth.models import User
from django.db import models

class CustomUser(User):
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=10, default='Bronze')
