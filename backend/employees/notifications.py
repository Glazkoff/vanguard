from patents.models import PatentPaymentReceipt, Patent
from .models import Employee, EmployeeInOrganization
from datetime import date, timedelta
from django.utils.html import format_html
from django.template import defaultfilters
from datetime import datetime


def go_through_patents():
    notifications = []
    patents = Patent.objects.all()
    for patent in patents:
        patentReceiptsQs = PatentPaymentReceipt.objects.filter(
            patent__id=patent.id).order_by('-paymentTermUntil')
        if len(patentReceiptsQs) > 0:
            patentExpirency = patentReceiptsQs[0].paymentTermUntil
            formatPatentExpirency = defaultfilters.date(
                patentExpirency, 'd E Y г.')
            d = date.today()+timedelta(days=14)
            if patentExpirency <= d:
                _ = patent.employee
                notifications.append('<a href="/admin/patents/patent/'+str(patent.id)+'/change/">Патент #'+str(
                    _.id)+'</a> сотрудника <a href="/admin/employees/employee/'+str(_.id)+'/change/">'+_.fullNameInGenetive+'</a> оплачен только до '+formatPatentExpirency+"!")
    employees = Employee.objects.all()
    for employee in employees:
        formatRegistrationValidityPeriod = defaultfilters.date(
            employee.registrationValidityPeriod, 'd E Y г.')
        formatEndDateOfRVP = defaultfilters.date(
            employee.endDateOfRVP, 'd E Y г.')
        formatEndDateOfResidencePermit = defaultfilters.date(
            employee.endDateOfResidencePermit, 'd E Y г.')
        d = date.today()+timedelta(days=14)
        if (
            employee.registrationValidityPeriod is not None
            and employee.registrationValidityPeriod <= d
        ):
            notifications.append('Регистрация сотрудника <a href="/employees/employee/'+str(employee.id)+'/change/">' +
                                 employee.fullNameInGenetive+'</a> действует только до ' + formatRegistrationValidityPeriod + "!")
        if (employee.endDateOfRVP is not None
                and employee.endDateOfRVP <= d):
            notifications.append('РВП сотрудника <a href="/admin/employees/employee/'+str(employee.id)+'/change/">' +
                                 employee.fullNameInGenetive+'</a> действует только до ' + formatEndDateOfRVP + "!")
        if (employee.endDateOfResidencePermit is not None and employee.endDateOfResidencePermit <= d):
            notifications.append('Вид на жительство сотрудника <a href="/admin/employees/employee/'+str(employee.id)+'/change/">' +
                                 employee.fullNameInGenetive+'</a> действует только до ' + formatEndDateOfResidencePermit + "!")
    return notifications


def action_set(obj):
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


def context_processor(request):
    extra_context = {}
    # if request.path == '//':
    extra_context['notifications'] = go_through_patents()
    employees = Employee.objects.all()
    for employee in employees:
        employee.actions = action_set(employee)
    extra_context['employees'] = employees
    return extra_context
