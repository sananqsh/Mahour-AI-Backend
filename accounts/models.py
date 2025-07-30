from django.contrib.auth.models import User
from django.db import models

class CustomUser(User):
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=10, default='Bronze')

    def get_name(self):
        name = ""
        if self.first_name:
            name = self.first_name
            if self.last_name:
                name = name + " " + self.last_name
        return name
