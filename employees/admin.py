from django.contrib import admin
from .models import Employee, EmployeeInOrganization


class EmployeeAdmin(admin.ModelAdmin):
    """Работники"""
    exclude = ('createdAt', 'updatedAt')


class EmployeeInOrganizationAdmin(admin.ModelAdmin):
    """Работники, прикрепленные к организациям"""
    exclude = ('createdAt', 'updatedAt')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeInOrganization, EmployeeInOrganizationAdmin)
