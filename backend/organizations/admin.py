from django.contrib import admin
from .models import Organization, Tariff, City
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export.formats import base_formats


class CityResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта городов"""
    class Meta:
        model = City

class CityAdmin(ImportExportModelAdmin):
    """Города"""
    list_display = ("cityName",)
    search_fields = ("cityName",)
    

class OrganizationResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта организации"""
    class Meta:
        model = Organization

class OrganizationAdmin(ImportExportModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress", "city")
    list_display_links = ("organizationName",)
    search_fields = ("organizationName",)
    ordering = ['-organizationName']
    
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
    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)


class TariffResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта патентов"""
    class Meta:
        model = Tariff

class TariffAdmin(ImportExportModelAdmin):
    """Тарифы"""
    list_display = ("positionName", "salaryPerHour", "kitchenOrHall", "city")
    list_display_links = ("positionName",)
    search_fields = ("positionName", "salaryPerHour",)
    ordering = ['-salaryPerHour']
    
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
    def get_queryset(self, request):
        qs = super(TariffAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)


admin.site.register(City, CityAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
