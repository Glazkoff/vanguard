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
from organizations.models import Organization

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
def mia_notifications_admission(request,employee_in_org_id):
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
    # - [X] working_document_number - номер документа (ОП)
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

    # - Таблицы в шаблоне:
    # - [X] mia_name_contents - название МВД (несколько строк,34 символа)
    # - [X] surname_contents - фамилия работника (одна строка,28 символов)
    # - [X] name_contents - имя работника (одна строка,28 символов)
    # - [X] patronymic_contents - отчетсво работника (одна строка,28 символов)
    # - [X] citizenship_contents - гражданство работника (одна строка,27 символов)
    # - [X] birthplace_contents - место рождения работника (несколько строк,24 символов)
    # - [X] birth_day_contents - день рождения работника 
    # - [X] birth_month_contents - месяц рождения работника 
    # - [X] birth_year_contents - год рождения работника 
    # - [X] type_identity_document_contents - тип документа (ДУЛ) (одна строка,19 символов)

    # - [X] series_identity_document_contents - серия документа (ДУЛ) (одна строка,7 символов)
    # - [X] number_identity_document_contents - номер документа (ДУЛ) (одна строка,9 символов)
    # - [X] identity_document_day_contents - день выдачи документа (ДУЛ)
    # - [X] identity_document_month_contents - месяц выдачи документа (ДУЛ)
    # - [X] identity_document_year_contents - год выдачи документа (ДУЛ)
    # - [X] identity_document_issued_by_contents - кем выдан документ (ДУЛ) (несколько строк,28 символов)
    # - [X] name_labor_activity_document_contents - название документа на трудовую деятельность (несколько строк,34 символа)
    # - [X] name_profession_contents - название профессии (несколько строк,34 символа)
    # - [X] contract_number_contents - номер ТД
    # - [X] contract_gph_number_contents - номер ГПХ
    # - [X] contract_start_day_contents - день заключения документа (ТД или ГПХ)
    # - [X] contract_start_month_contents - месяц заключения документа (ТД или ГПХ)
    # - [X] contract_start_year_contents - год заключения документа (ТД или ГПХ)
    # - [X] legal_organization_address_contents - адрес организации (несколько строк,34 символа)
    
    employeeInOrg = EmployeeInOrganization.objects.get(
            pk=employee_in_org_id)
    employee = Employee.objects.get(pk=employeeInOrg.employee_id)
    organization = Organization.objects.get(pk=employeeInOrg.organization_id)
    full_name_split = employee.fullName.split()
    name_split_content = full_name_split[1]
    surname_split_content = full_name_split[0]
    patronymic_split_content = full_name_split[2]
    contract_date = ' '
    if employeeInOrg.employmentContractNumber == None:
        contract_date = employeeInOrg.startDateOfGPHContract
    else: 
        contract_date = employeeInOrg.employmentContractDate
    

    # Разделение тексовых данных на элементы
    def split_data(data,count_col):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        for i in range(count_col-count_data_split):
            data_split.append('   ')
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
        output_data = [data_split[x - y: x] for x, y in zip(accumulate(length_to_split), length_to_split)]
        for i in range(len(output_data)):
            if (len(output_data[i])<count_col):
                for k in range(count_col-len(output_data[i])):
                    output_data[i].append('   ')
        return output_data[number_row-1]

    # Проверка работает ли сотрудник по ТД или по ГПХ
    def contract_check(contract_number):
        mark_contract = " "
        if (contract_number == None):
            mark_contract = " "
            return mark_contract
        if (contract_number != None):
            mark_contract = "X"
            return mark_contract

    context = {
    'mia_name_contents': [
        {'cols': split_data_rows("овм му мвд россии балашихинское",count_col = 34,number_row = 1)},
        {'cols': split_data_rows("овм му мвд россии балашихинское",count_col = 34,number_row = 2)},
        {'cols': split_data_rows("овм му мвд россии балашихинское",count_col = 34,number_row = 3)},
    ],
    'surname_contents': [
        {'cols': split_data(surname_split_content,28)}
    ],
    'name_contents': [
        {'cols': split_data(name_split_content,28)}
    ],
    'patronymic_contents': [
        {'cols': split_data(patronymic_split_content,28)}
    ],
    'citizenship_contents': [
        {'cols': split_data(employee.citizenship,27)}
    ],
    'birthplace_contents': [
        {'cols': split_data_rows(employee.birthplace,count_col = 24,number_row = 1)},
        {'cols': split_data_rows(employee.birthplace,count_col = 24,number_row = 2)},
        {'cols': split_data_rows(employee.birthplace,count_col = 24,number_row = 3)},
    ],
    'birth_day_contents': [
        {'cols': split_day(defaultfilters.date(employee.birthday, 'd.m.Y'))}
    ],
    'birth_mouth_contents': [
        {'cols': split_month(defaultfilters.date(employee.birthday, 'd.m.Y'))}
    ],
    'birth_year_contents': [
        {'cols': split_year(defaultfilters.date(employee.birthday, 'd.m.Y'))}
    ],
    'type_identity_document_contents': [
        {'cols': split_data("паспорт",19)}
    ],
    'series_identity_document_contents': [
        {'cols': split_data("1234567",7)}
    ],
    'number_identity_document_contents': [
        {'cols': split_data(employee.passportNumber,9)}
    ],
    'identity_document_day_contents': [
        {'cols': split_day(defaultfilters.date(employee.passportIssueDate, 'd.m.Y'))}
    ],
    'identity_document_month_contents': [
        {'cols': split_month(defaultfilters.date(employee.passportIssueDate, 'd.m.Y'))}
    ],
    'identity_document_year_contents': [
        {'cols': split_year(defaultfilters.date(employee.passportIssueDate, 'd.m.Y'))}
    ],
    'identity_document_issued_by_contents': [
        {'cols': split_data_rows(employee.passportIssuedBy,count_col = 28,number_row = 1)},
        {'cols': split_data_rows(employee.passportIssuedBy,count_col = 28,number_row = 2)},
        {'cols': split_data_rows(employee.passportIssuedBy,count_col = 28,number_row = 3)},
    ],
    'name_labor_activity_document_contents': [
        {'cols': split_data_rows("Договор ЕАЭС от 29.04.2014",count_col = 34,number_row = 1)},
        {'cols': split_data_rows("Договор ЕАЭС от 29.04.2014",count_col = 34,number_row = 2)},
        {'cols': split_data_rows("Договор ЕАЭС от 29.04.2014",count_col = 34,number_row = 3)},
    ],
    'contract_number_contents': [
        {'cols': contract_check(employeeInOrg.employmentContractNumber)}
    ],
    'contract_gph_number_contents': [
        {'cols': contract_check(employeeInOrg.GPHContractNumber)}
    ],
    'contract_start_day_contents': [
        {'cols': split_day(defaultfilters.date(contract_date, 'd.m.Y'))}
    ],
    'contract_start_mouth_contents': [
        {'cols': split_month(defaultfilters.date(contract_date, 'd.m.Y'))}
    ],
    'contract_start_year_contents': [
        {'cols': split_year(defaultfilters.date(contract_date, 'd.m.Y'))}
    ],
    'legal_organization_address_contents': [
        {'cols': split_data_rows(organization.legalOrganizationAddress,count_col = 34,number_row = 1)},
        {'cols': split_data_rows(organization.legalOrganizationAddress,count_col = 34,number_row = 2)},
        {'cols': split_data_rows(organization.legalOrganizationAddress,count_col = 34,number_row = 3)},
    ],
    'name_profession_contents': [
        {'cols': split_data_rows("Работник пб",count_col = 34,number_row = 1)},
        {'cols': split_data_rows("Работник пб",count_col = 34,number_row = 2)},
        {'cols': split_data_rows("Работник пб",count_col = 34,number_row = 3)},
    ],
}

    doc.render(context)
    doc_io = io.BytesIO() 
    doc.save(doc_io)
    doc_io.seek(0)

    response = HttpResponse(doc_io.read())

    now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
    filename = f"Уведомление_МВД_о_приеме_{employee.fullNameInGenetive}_{now}"
    filename = escape_uri_path(filename)
    response["Content-Disposition"] = f"attachment; filename={filename}.doc"
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response
