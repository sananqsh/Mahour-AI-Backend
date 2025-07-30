from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=10, default='Bronze')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_name(self):
        name = ""
        if self.first_name:
            name = self.first_name
            if self.last_name:
                name = name + " " + self.last_name
        return name
