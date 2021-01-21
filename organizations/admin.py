from django.contrib import admin
from .models import Organization, Tariff


class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress")
    
    def get_queryset(self, request):
        qs = super(OrganizationAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)



class TariffAdmin(admin.ModelAdmin):
    """Тарифы"""
    list_display = ("organization", "positionName", "salaryPerHour")
    list_filter = ("organization",)
    search_fields = ("organization", "positionName")
    
    def get_queryset(self, request):
        qs = super(TariffAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
