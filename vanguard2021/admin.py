from django.contrib import admin
from .models import Employee, Organization, Tariff, EmployeeInOrganization, Patent, PatentPaymentReceipt

class EmployeeAdmin(admin.ModelAdmin):
    """Работники"""
    exclude = ('createdAt', 'updatedAt')

class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ("organizationName", "legalOrganizationAddress")

class TariffAdmin(admin.ModelAdmin):
    """Тарифы"""
    list_display = ("organization", "positionName", "salaryPerHour")

class EmployeeInOrganizationAdmin(admin.ModelAdmin):
    """Работники, прикрепленные к организациям"""
    exclude = ('createdAt', 'updatedAt')

class PatentAdmin(admin.ModelAdmin):
    """Патенты"""
    list_display = ('employee', 'dateOfPatentIssue')
    
class PatentPaymentReceiptAdmin(admin.ModelAdmin):
    """Квитанция оплаты патента"""
    list_display = ('patent', 'paymentTermFrom', 'paymentTermUntil')
    

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(EmployeeInOrganization, EmployeeInOrganizationAdmin)
admin.site.register(Patent, PatentAdmin)
admin.site.register(PatentPaymentReceipt, PatentPaymentReceiptAdmin)

