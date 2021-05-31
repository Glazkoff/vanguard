from django.contrib import admin
from .models import Organization, Tariff
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class OrganizationResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта патентов"""
    class Meta:
        model = Organization

class OrganizationAdmin(ImportExportModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress", "cityOrganization")
    list_display_links = ("organizationName",)
    search_fields = ("organizationName",)
    ordering = ['-organizationName']
    
    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)


class TariffResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта патентов"""
    class Meta:
        model = Tariff

class TariffAdmin(ImportExportModelAdmin):
    """Тарифы"""
    list_display = ("organization", "positionName", "salaryPerHour")
    list_filter = ("organization__organizationName",)
    list_display_links = ("positionName",)
    search_fields = ("organization__organizationName",
                     "positionName", "salaryPerHour",)
    ordering = ['-salaryPerHour']
    
    def get_queryset(self, request):
        qs = super(TariffAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
