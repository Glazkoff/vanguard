from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import Employee, EmployeeInOrganization

class EmployeeResource(resources.ModelResource):
    """Ресурс сотрудника для импорта"""
    class Meta:
        model = Employee

class EmployeeAdmin(ImportExportModelAdmin):
    """Работники"""
    exclude = ('createdAt', 'updatedAt')
    # list_display=('')
    list_filter = ('birthday','citizenship','registrationValidityPeriod','dateOfNotificationUFMSadmission','dateOfNotificationUFMSdischarge', 'endDateOfResidencePermit', 'endDateOfRVP')
    search_fields=('fullName','fullNameInGenetive')
    fieldsets = (
        (None, {
            'fields': (('fullName','fullNameInGenetive'), 'birthday','phoneNumber',('INN','SNILS'),'bankDetails', ('endDateOfResidencePermit', 'endDateOfRVP'))
        }),
        ('Данные паспорта', {
            'fields': (('passportNumber','passportValidityPeriod'),'citizenship', 'passportIssuedBy')
        }),
        ('Данные о регистрации', {
            'fields': ( 'registrationValidityPeriod','registrationAddress')
        }),
        ('Данные из УФМС', {
            'fields': ('dateOfNotificationUFMSadmission', 'dateOfNotificationUFMSdischarge')
        }),
    )
    resource_class = EmployeeResource

    def get_queryset(self, request):
        qs = super(EmployeeAdmin, self).get_queryset(request)
        return qs.filter(deleted=False)


class EmployeeInOrganizationResource(resources.ModelResource):
    """Ресурс сотрудника в организации для импорта"""
    class Meta:
        model = EmployeeInOrganization

class EmployeeInOrganizationAdmin(ImportExportModelAdmin):
    """Работники, прикрепленные к организациям"""
    exclude = ('createdAt', 'updatedAt')
    list_filter = ('tariff','organization__organizationName')
    search_fields=('tariff__positionName','organization__organizationName')
    resource_class = EmployeeInOrganizationResource


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeInOrganization, EmployeeInOrganizationAdmin)
admin.site.site_title = "Авангард"
admin.site.site_header = "Авангард"