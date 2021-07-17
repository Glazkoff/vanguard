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
from itertools import accumulate 

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
        if employeeInOrg.tariff.kitchenOrHall == "kitchen":
            employee_work_place += "кухня"
        else:
            employee_work_place += "зал"
        context = {
            'contract_number': employeeInOrg.employmentContractNumber,
            'today': defaultfilters.date(datetime.datetime.today(), '«d» E Y г.'),
            'employee_citizenship': employee.citizenship,
            'employee_full_name': employee.fullName,
            'employee_work_place': employee_work_place,
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
def mia_notifications_admission(request):
    # os.path.dirname(employees.__file__)
    doc = DocxTemplate(os.path.join(
        APP_ROOT, "docs", "mia_notification_admission.docx"))
    # Получить:
    # - [%] surname - фамилия
    # - [%] name - имя
    # - [%] patronymic - отчество
    # - [] citizenship - гражданство
    # - [] birthplace - место рождения
    # - [] birthday - дата рождения
    # - [%] identity_document - название документа, удостоверяющий личность (ДУЛ)
    # - [%] identity_document_series - серия документа (ДУЛ)
    # - [] identity_document_number - номер документа (ДУЛ)
    # - [] identity_document_issue_date - дата выдачи документа (ДУЛ)
    # - [] identity_document_issued_by - кем выдан документ (ДУЛ)
    # - [] working_document - наименование документа об обосновании на прием (ОП)
    # - [] working_document_series - серия документа (ОП)
    # - [] working_document_number - номер документа (ОП)
    # - [] working_document_issue_date - дата выдачи документа (ОП)
    # - [] working_document_issued_by - кем выдан документ (ОП)
    # - [] working_document_term_from - срок действия документа от (ОП)
    # - [] working_document_term_until - срок действия документа до (ОП)
    # - [] contract - на основании какого документа работает (ТД или ГПХ)
    # - [] contract_start_date - дата заключение (ТД или ГПХ)
    # - [] legal_organization_address - адрес организации

    # - Отсутствуют в БД:
    # - [] Наименование МВД
    # - [] Документ на трудовую деятельность
    # - [] Название профессии (возможно, нужно какое-то особое название для уведомлений)

    # Разделение тексовых данных на элементы
    def split_data(data,count_col):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        for i in range(count_col-count_data_split):
            data_split.append(' ')
        return data_split

    # Получения дня из даты
    def split_day(date):
        date_split = date.split(".")
        day = list(date_split[0])
        return day 

    # Получения месяца из даты
    def split_month(date):
        date_split = date.split(".")
        month = list(date_split[1])
        return month

    # Получения года из даты
    def split_year(date):
        date_split = date.split(".")
        year = list(date_split[2])
        return year

    # Разделение данных на несколько строк
    def split_data_rows (data, count_col,number_row):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        length_to_split = [count_col, count_col, count_col]
        Output = [data_split[x - y: x] for x, y in zip(accumulate(length_to_split), length_to_split)]
        for i in range(len(Output)):
            if (len(Output[i])<34):
                for k in range(34-len(Output[i])):
                    Output[i].append(' ')
        return Output[number_row-1]

    # Проверка работает ли сотрудник по ТД
    def contract_check(contract_number):
        mark_contract = " "
        if (contract_number == " "):
            mark_contract = " "
            return mark_contract
        if (contract_number != " "):
            mark_contract = "X"
            return mark_contract
    
    # Проверка работает ли сотрудник по ГПХ
    def gph_contract_check(gph_contract_number):
        mark_gph_contract = " "
        if (gph_contract_number == " "):
            mark_gph_contract = " "
            return mark_gph_contract
        if (gph_contract_number != " "):
            mark_gph_contract = "X"
            return mark_gph_contract

    context = {
    'tbl_contents': [
        {'cols': contract_check(contract_number=" ")}
    ],
    'tbl_contents1': [
        {'cols': gph_contract_check(gph_contract_number=1111111111)}
    ],
    
}

    doc.render(context)
    doc_io = io.BytesIO() 
    doc.save(doc_io)
    doc_io.seek(0)

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response
