from django.contrib import admin

from .models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'date')

    def total(self, obj):
        return obj.get_total()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")

@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    list_display = ("user",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("inbox", "title", "date", "read_flag")
