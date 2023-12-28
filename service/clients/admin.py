from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    pass
