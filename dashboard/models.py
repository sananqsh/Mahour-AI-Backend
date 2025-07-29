from django.db import models
from django.db.models.aggregates import Sum

from accounts.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=100)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.FloatField()
    date = models.DateField()
    items = models.ManyToManyField(Product)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.total = self.items.aggregate(total=Sum('price'))['total']

class Inbox(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Message(models.Model):
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateField()
    read_flag = models.BooleanField(default=False)

    def mark_as_read(self):
        self.read_flag = True
        self.save()
