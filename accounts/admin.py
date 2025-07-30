from django.contrib import admin

from .models import CustomUser

@admin.register(CustomUser)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "points", "tier",)

    def name(self, obj):
        return obj.get_name()
