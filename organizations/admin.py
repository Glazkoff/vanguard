from django.contrib import admin
from .models import Organization, Tariff


class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress")


class TariffAdmin(admin.ModelAdmin):
    """Тарифы"""
    list_display = ("organization", "positionName", "salaryPerHour")
    list_filter = ("organization",)
    search_fields = ("organization", "positionName")


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
