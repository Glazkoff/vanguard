import io
import os
import os.path
import tempfile
import zipfile
import datetime
import employees
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import escape_uri_path
from vanguard.settings import MEDIA_ROOT
from .models import Employee, EmployeeInOrganization
from docxtpl import DocxTemplate
from django.template import defaultfilters
from number_to_string import get_string_by_number

APP_ROOT = os.path.abspath(os.path.dirname(__file__))


@login_required(login_url='/admin')
def doc_test(request):
    # os.path.dirname(employees.__file__)
    doc = DocxTemplate(os.path.join(
        APP_ROOT, "docs", "test_1.docx"))
    # ... your other code ...
    context = {'title': "NGLAZKOV one file"}
    doc.render(context)
    doc_io = io.BytesIO()  # create a file-like object
    doc.save(doc_io)  # save data to file-like object
    doc_io.seek(0)  # go to the beginning of the file-like object

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response


def generate_zip(files):
    mem_zip = io.BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()


@login_required(login_url='/admin')
def doc_multiple_test(request):
    files = []

    for i in range(5):
        doc = DocxTemplate(os.path.join(APP_ROOT, "docs", "test_1.docx"))
        # ... your other code ...
        context = {'title': "NGLAZKOV company - multiple " + str(i) + " tests"}
        doc.render(context)
        doc_io = io.BytesIO()  # create a file-like object
        doc.save(doc_io)  # save data to file-like object
        doc_io.seek(0)  # go to the beginning of the file-like object
        files.append(("test"+str(i)+".docx", doc_io.getvalue()))

    full_zip_in_memory = generate_zip(files)

    response = HttpResponse(full_zip_in_memory, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    return response


@login_required(login_url='/admin')
def labor_contract(request, employee_in_org_id):
    doc = DocxTemplate(os.path.join(
        APP_ROOT, "docs", "1_labor_contract.doc"))
    # Получить:
    # - [x] contract_number - номер трудового договора
    # - [x] today - дата сегодня
    # - [x] employee_citizenship - гражданство работника
    # - [x] employee_full_name - ФИО работника
    # - [x] employee_work_place - место работы (кухня/зал) ???
    # - [x] work_start_day -  дата начала работы
    # - [x] tariff - тарифная ставка
    # - [x] tariff_by_words - тарифная ставка словами
    # - [x] employee_passport_number - номер папорта работника
    # - [x] employee_passport_date_of_issue- дата выдачи паспорта работника
    # - [x] employee_snils - СНИЛС работника
    # - [x] employee_inn - ИНН работника

    try:
        employeeInOrg = EmployeeInOrganization.objects.get(
            pk=employee_in_org_id)
        employee = Employee.objects.get(pk=employeeInOrg.employee.id)
        employee_work_place = ""
        # if employeeInOrg.tariff.kitchenOrHall == "kitchen":
        #     employee_work_place += "кухня"
        # else:
        #     employee_work_place += "зал"
        context = {
            'contract_number': employeeInOrg.employmentContractNumber,
            'today': defaultfilters.date(datetime.datetime.today(), '«d» E Y г.'),
            'employee_citizenship': employee.citizenship,
            'employee_full_name': employee.fullName,
            'employee_work_place': employeeInOrg.organization.legalOrganizationAddress,
            'work_start_date': defaultfilters.date(employeeInOrg.admissionDate, '«d» E Y г.'),
            'tariff': employeeInOrg.tariff.salaryPerHour,
            'tariff_by_words': get_string_by_number(employeeInOrg.tariff.salaryPerHour),
            'employee_passport_number': employee.passportNumber,
            'employee_passport_date_of_issue': defaultfilters.date(employee.passportIssueDate, 'd E Y г.'),
            'employee_snils': employee.SNILS,
            'employee_inn': employee.INN
        }
    except EmployeeInOrganization.DoesNotExist:
        html = "<html><body><h1 style='font-family: sans-serif;'>Работник в организации не найден!</h1></body></html>"
        return HttpResponse(html)

    doc.render(context)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    response = HttpResponse(doc_io.read())

    now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
    filename = f"Трудовой_договор_{employee.fullNameInGenetive}_{now}"
    filename = escape_uri_path(filename)
    response["Content-Disposition"] = f"attachment; filename={filename}.doc"
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response

@login_required(login_url='/admin')
def gph_contract(request, employee_in_org_id):
    doc = DocxTemplate(os.path.join(
        APP_ROOT, "docs", "gph.docx"))
    try:
        employeeInOrg = EmployeeInOrganization.objects.get(
            pk=employee_in_org_id)
        employee = Employee.objects.get(pk=employeeInOrg.employee.id)
        context = {
            'employee_full_name': employee.fullName,
            'today': defaultfilters.date(datetime.datetime.today(), '«d» E Y г.'),
            'employee_work_place': employeeInOrg.organization.legalOrganizationAddress,
            'end_date_gph_contract': defaultfilters.date(employeeInOrg.endDateOfGPHContract, 'd E Y г.'),
            'employee_passport_number': employee.passportNumber,
            'employee_passport_issued_by': employee.passportIssuedBy,
            'employee_passport_date_of_issue': defaultfilters.date(employee.passportIssueDate, 'd E Y г.'),
            'employee_registration_address': employee.registrationAddress,
            'employee_inn': employee.INN, 
            'employee_phone': employee.phoneNumber
        }
    except EmployeeInOrganization.DoesNotExist:
        html = "<html><body><h1 style='font-family: sans-serif;'>Работник в организации не найден!</h1></body></html>"
        return HttpResponse(html)

    doc.render(context)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    response = HttpResponse(doc_io.read())

    now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
    filename = f"Договор_ГПХ_{employee.fullNameInGenetive}_{now}"
    filename = escape_uri_path(filename)
    response["Content-Disposition"] = f"attachment; filename={filename}.docx"
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response