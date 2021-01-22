from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import Employee, EmployeeInOrganization
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class EmployeeResource(resources.ModelResource):
    """Ресурс сотрудника для импорта"""
    class Meta:
        model = Employee

class EmployeeAdmin(ImportExportModelAdmin):
    """Работники"""
    list_display = ("fullName", "fullNameInGenetive","birthday","passportNumber","passportIssuedBy","passportValidityPeriod","citizenship","phoneNumber","INN","SNILS","registrationAddress","registrationValidityPeriod","dateOfNotificationMVDadmission","dateOfNotificationMVDdischarge","bankDetails")
    exclude = ('createdAt', 'updatedAt')
    list_filter = ('citizenship',('registrationValidityPeriod',DateRangeFilter),('dateOfNotificationMVDadmission',DateRangeFilter),('dateOfNotificationMVDdischarge',DateRangeFilter))
    search_fields=('fullName','fullNameInGenetive')
    fieldsets = (
        (None, {
            'fields': (('fullName','fullNameInGenetive'), 'birthday','phoneNumber',('INN','SNILS'),'bankDetails')
        }),
        ('Данные паспорта', {
            'fields': (('passportNumber','passportValidityPeriod'),'citizenship', 'passportIssuedBy')
        }),
        ('Данные о регистрации', {
            'fields': ( 'registrationValidityPeriod','registrationAddress')
        }),
        ('Данные из МВД', {
            'fields': ('dateOfNotificationMVDadmission', 'dateOfNotificationMVDdischarge')
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