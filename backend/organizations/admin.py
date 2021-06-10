from django.contrib import admin
from .models import Organization, Tariff, City
from import_export.admin import ImportExportModelAdmin
from import_export import resources

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
    
class TariffResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта патентов"""
    class Meta:
        model = Tariff

class TariffAdmin(ImportExportModelAdmin):
    """Тарифы"""
    list_display = ("positionName", "salaryPerHour", "kitchenOrHall", "city")
    # list_filter = ("city__cityName",)
    list_display_links = ("positionName",)
    search_fields = ("positionName", "salaryPerHour",)
    ordering = ['-salaryPerHour']
    
admin.site.register(City, CityAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
