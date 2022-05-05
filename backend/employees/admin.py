from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import Employee, EmployeeInOrganization
from admin_interface.models import Theme
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export.formats import base_formats
from django.utils.html import format_html
from django.shortcuts import render


class EmployeeResource(resources.ModelResource):
    """Ресурс сотрудника для импорта"""
    class Meta:
        model = Employee


class EmployeeAdmin(ImportExportModelAdmin):
    """Работники"""
    exclude = ('createdAt', 'updatedAt')
    list_filter = ('company', 'birthday', 'citizenship', ('registrationValidityPeriod', DateRangeFilter), ('dateOfNotificationUFMSadmission', DateRangeFilter),
                   ('dateOfNotificationUFMSdischarge', DateRangeFilter), ('endDateOfResidencePermit', DateRangeFilter), ('endDateOfRVP', DateRangeFilter))
    search_fields = ('name', 'surname', 'patronymic', 'fullNameInGenetive')
    fieldsets = (
        (None, {
            'fields': ('company', 'surname', 'name', 'patronymic', 'fullNameInGenetive', 'birthday', 'birthplace', 'phoneNumber', ('INN', 'SNILS'), ('endDateOfResidencePermit', 'endDateOfRVP'))
        }),
        #  ('Место рождения', {
        #     'fields': ('birthplace_country', 'birthplace_subject','birthplace_city', 'birthplace_locality', 'birthplace_street','birthplace_home','birthplace_home_expansion' )
        # }),
        ('Банковские данные', {
            'fields': (('bankDetailsNameBank', 'bankDetailsCardNumber'), ('bankDetailsPaymentAccount', 'bankDetailsBIC'))
        }),
        ('Данные паспорта', {
            'fields': (('passportSeries', 'passportNumber', 'passportValidityPeriod'), 'citizenship', 'passportIssuedBy', 'passportIssueDate')
        }),
        ('Данные о регистрации', {
            'fields': ('registrationValidityPeriod', 'registrationAddress')
        }),
        ('Данные из УФМС', {
            'fields': ('nameMIA', 'dateOfNotificationUFMSadmission', 'dateOfNotificationUFMSdischarge')
        }),
    )
    resource_class = EmployeeResource

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
    # def get_queryset(self, request):
    #     qs = super(EmployeeAdmin, self).get_queryset(request)
    #     return qs.filter(deleted=False)

    def action_set(self, obj):
        tag_string = ""
        employeeInOrganizations = EmployeeInOrganization.objects.filter(
            employee=obj)
        for empInOrg in employeeInOrganizations:
            tag_string += f'<a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/labor_contract/{empInOrg.id}">Сформировать трудовой договор ({empInOrg.tariff.positionName})</a>'
            tag_string += f'<br /><a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/gph_contract/{empInOrg.id}">Сформировать договор ГПХ</a>'
            if empInOrg.employmentContractDate is not None or empInOrg.startDateOfGPHContract is not None:
                tag_string += f'<br /><a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/mia_notifications_admission/{empInOrg.id}">Сформировать уведомление в МВД о приеме</a>'
            if empInOrg.dischargeDate is not None:
                tag_string += f'<br /><a target="_blank" style="margin-bottom: 1rem;" href="/api/documents/mia_notification_discharge/{empInOrg.id}">Сформировать уведомление в МВД об увольнении</a>'
        return format_html(tag_string)

    action_set.short_description = "Действия"
    # action_set.admin_order_field = '_last_payment_receipt'
    list_display = ('__str__', 'company', 'action_set',
                    'registrationValidityPeriod', 'createdAt')


class EmployeeInOrganizationResource(resources.ModelResource):
    """Ресурс сотрудника в организации для импорта"""
    class Meta:
        model = EmployeeInOrganization


class EmployeeInOrganizationAdmin(ImportExportModelAdmin):
    """Работники, прикрепленные к организациям"""
    exclude = ('createdAt', 'updatedAt')
    list_filter = ('tariff__positionName',
                   'organization__organizationName', 'city__cityName',)
    search_fields = ('tariff__positionName',
                     'organization__organizationName', 'city__cityName',)
    resource_class = EmployeeInOrganizationResource

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
    # def get_queryset(self, request):
    #     qs = super(EmployeeInOrganizationAdmin, self).get_queryset(request)
    #     return qs.filter(deleted=False)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeInOrganization, EmployeeInOrganizationAdmin)
admin.site.unregister(Theme)
admin.site.site_title = "Авангард"
admin.site.site_header = "Авангард"
admin.site.index_title = "Авангард"
admin.site.index_template = "admin/custom_index.html"
admin.autodiscover()
