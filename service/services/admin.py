from django.contrib import admin

from services.models import Plan, Service, Subscription


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class ServiceAdmin(admin.ModelAdmin):
    pass
