from django.contrib import admin
from .models import Organization, Tariff
from import_export.formats import base_formats

class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress")
    
    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)
    def get_export_formats(self):
            formats = (
                  base_formats.XLS,
                  base_formats.XLSX,
            )
            return [f for f in formats if f().can_export()]
    def get_import_formats(self):
            formats = (
                  base_formats.XLS,
                  base_formats.XLSX,
            )
            return [f for f in formats if f().can_import()]


class TariffAdmin(admin.ModelAdmin):
    """Тарифы"""
    list_display = ("organization", "positionName", "salaryPerHour")
    list_filter = ("organization",)
    search_fields = ("organization", "positionName")
    
    def get_queryset(self, request):
        qs = super(TariffAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)
    def get_export_formats(self):
            formats = (
                  base_formats.XLS,
                  base_formats.XLSX,
            )
            return [f for f in formats if f().can_export()]
    def get_import_formats(self):
            formats = (
                  base_formats.XLS,
                  base_formats.XLSX,
            )
            return [f for f in formats if f().can_import()]

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
