from django.contrib import admin
from .models import Organization, Tariff


class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress")
    list_display_links = ("organizationName",)
    search_fields = ("organizationName", )


class TariffAdmin(admin.ModelAdmin):
    """Тарифы"""
    list_display = ("organization", "positionName", "salaryPerHour")
    list_filter = ("organization__organizationName",)
    list_display_links = ("positionName",)
    search_fields = ("organization__organizationName",
                     "positionName", "salaryPerHour",)
    ordering = ['-salaryPerHour']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
