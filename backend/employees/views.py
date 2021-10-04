import io
import os
import os.path
import zipfile
import datetime
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
from patents.models import Patent

APP_ROOT = os.path.abspath(os.path.dirname(__file__))


# @login_required(login_url='/admin')
# def doc_test(request):
#     doc = DocxTemplate(os.path.join(
#         APP_ROOT, "docs", "test_1.docx"))
#     # ... your other code ...
#     context = {'title': "NGLAZKOV one file"}
#     doc.render(context)
#     doc_io = io.BytesIO()  # create a file-like object
#     doc.save(doc_io)  # save data to file-like object
#     doc_io.seek(0)  # go to the beginning of the file-like object

#     response = HttpResponse(doc_io.read())

#     # Content-Disposition header makes a file downloadable
#     response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

#     # Set the appropriate Content-Type for docx file
#     response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

#     return response


# def generate_zip(files):
#     mem_zip = io.BytesIO()

#     with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
#         for f in files:
#             zf.writestr(f[0], f[1])

#     return mem_zip.getvalue()


# @login_required(login_url='/admin')
# def doc_multiple_test(request):
#     files = []

#     for i in range(5):
#         doc = DocxTemplate(os.path.join(APP_ROOT, "docs", "test_1.docx"))
#         # ... your other code ...
#         context = {'title': "NGLAZKOV company - multiple " + str(i) + " tests"}
#         doc.render(context)
#         doc_io = io.BytesIO()  # create a file-like object
#         doc.save(doc_io)  # save data to file-like object
#         doc_io.seek(0)  # go to the beginning of the file-like object
#         files.append(("test"+str(i)+".docx", doc_io.getvalue()))

#     full_zip_in_memory = generate_zip(files)

#     response = HttpResponse(full_zip_in_memory, content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename=test.zip'
#     return response


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
        try:
            patent = Patent.objects.get(employee=Employee.objects.get(pk=employeeInOrg.employee_id))
        except Patent.DoesNotExist:
            patent = []
        employee_reason_work = ""
        if employeeInOrg.reasonWorkEmployee == 'EAEU':
            employee_reason_work = "на основании договора ЕАЭС от 29.04.2014"
        if employeeInOrg.reasonWorkEmployee == 'P':
            employee_reason_work = "на основании патента № "+patent.patentNumber+" серии "+patent.patentSeries+", который выдан " + patent.patentIssuedBy + \
                " сроком от "+defaultfilters.date(patent.dateOfPatentIssue, 'd E Y г.') + \
                " до " + \
                defaultfilters.date(
                    patent.dateExpirationPatent, 'd E Y г.')+" ."
        employee_work_place = ""
        # if employeeInOrg.tariff.kitchenOrHall == "kitchen":
        #     employee_work_place += "кухня"
        # else:
        #     employee_work_place += "зал"

        context = {
            'employee_citizenship':  (f"{employee.citizenship}", "")[employee.citizenship is None],
            'employee_reason_work': employee_reason_work,
            'employee_full_name': (f"{employee.surname} {employee.name} {employee.patronymic}", f"{employee.surname} {employee.name}")[employee.patronymic is None],
            'employee_work_place': (f"{employeeInOrg.organization.legalOrganizationAddress}", "")[employeeInOrg.organization.legalOrganizationAddress is None],
            'work_start_date': (defaultfilters.date(employeeInOrg.admissionDate, '«d» E Y г.'), "")[employeeInOrg.admissionDate is None],
            'tariff': (f"{employeeInOrg.tariff.salaryPerHour}", "")[employeeInOrg.tariff.salaryPerHour is None],
            'tariff_by_words': get_string_by_number((f"{employeeInOrg.tariff.salaryPerHour}", "")[employeeInOrg.tariff.salaryPerHour is None]),
            'employee_passport_number': (f"{employee.passportNumber}", "—")[employee.passportNumber is None],
            'employee_passport_series': (f"{employee.passportSeries}", "—")[employee.passportSeries is None or employee.passportSeries == ""],
            'employee_passport_date_of_issue': (defaultfilters.date(employee.passportIssueDate, 'd E Y г.'), "")[employee.passportIssueDate is None],
            'employee_snils': (f"{employee.SNILS}", "—")[employee.SNILS is None],
            'employee_inn': (f"{employee.INN}", "—")[employee.INN is None]
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
        employee = Employee.objects.get(pk=employeeInOrg.employee_id)
        context = {
            'employee_full_name': (f"{employee.surname} {employee.name} {employee.patronymic}", f"{employee.surname} {employee.name}")[employee.patronymic is None],
            'today': defaultfilters.date(datetime.datetime.today(), '«d» E Y г.'),
            'employee_work_place': (f"{employeeInOrg.organization.legalOrganizationAddress}", "")[employeeInOrg.organization.legalOrganizationAddress is None],
            'end_date_gph_contract': (defaultfilters.date(employeeInOrg.endDateOfGPHContract, 'd E Y г.'), "")[employeeInOrg.endDateOfGPHContract is None],
            'employee_passport_series':  (f"серия {employee.passportSeries}  № ", "")[employee.passportSeries is None],
            'employee_passport_number': (f"{employee.passportNumber}", "")[employee.passportNumber is None],
            'employee_passport_issued_by': (f"{employee.passportIssuedBy}", "")[employee.passportIssuedBy is None],
            'employee_passport_date_of_issue': (defaultfilters.date(employee.passportIssueDate, 'd E Y г.'), "")[employee.passportIssueDate is None],
            'employee_registration_address': (f"{employee.registrationAddress}", "")[employee.registrationAddress is None],
            'employee_inn': (f"{employee.INN}", "")[employee.INN is None],
            'employee_phone': (f"{employee.phoneNumber}", "")[employee.phoneNumber is None],
            'tariff': (f"{employeeInOrg.tariff.salaryPerHour}", "")[employeeInOrg.tariff.salaryPerHour is None],
            'tariff_by_words': (get_string_by_number(employeeInOrg.tariff.salaryPerHour), "")[employeeInOrg.tariff.salaryPerHour is None],

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

# Уведомление МВД о приеме


@login_required(login_url='/admin')
def mia_notifications_admission(request, employee_in_org_id):
    # os.path.dirname(employees.__file__)
    doc = DocxTemplate(os.path.join(
        APP_ROOT, "docs", "mia_notification_admission.docx"))
    # Получить:
    # - [X] surname - фамилия
    # - [X] name - имя
    # - [X] patronymic - отчество
    # - [X] citizenship - гражданство
    # - [X] birthplace - место рождения
    # - [X] birthday - дата рождения
    # - [@] identity_document - название документа, удостоверяющий личность (ДУЛ)
    # - [X] identity_document_series - серия документа (ДУЛ)
    # - [X] identity_document_number - номер документа (ДУЛ)
    # - [X] identity_document_issue_date - дата выдачи документа (ДУЛ)
    # - [X] identity_document_issued_by - кем выдан документ (ДУЛ)
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
    # - [X] Наименование МВД
    # - [] Документ на трудовую деятельность
    # - [X] Название профессии (возможно, нужно какое-то особое название для уведомлений)

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

    # Получение данных из моделей
    employeeInOrg = EmployeeInOrganization.objects.get(
        pk=employee_in_org_id)
    employee = Employee.objects.get(pk=employeeInOrg.employee_id)
    try:
        patent = Patent.objects.get(employee=Employee.objects.get(pk=employeeInOrg.employee_id))
    except Patent.DoesNotExist:
        patent = []

    organization = Organization.objects.get(pk=employeeInOrg.organization_id)

    # Проверка наличия отчества
    if employee.patronymic is None:
        local_patronymic = ""
    else:
        local_patronymic = employee.patronymic

    # Проверка наличия ТД или ГПХ
    contract_date = ' '
    if employeeInOrg.employmentContractNumber == None:
        contract_date = employeeInOrg.startDateOfGPHContract
    else:
        contract_date = employeeInOrg.employmentContractDate

    # Получение полного адреса организация (с индексом)
    all_address = organization.postCodeOrganization + \
        " " + organization.legalOrganizationAddress

    # Получения данных о патенте
    name_patent_document = ""
    patent_number = ""
    patent_series = ""
    patent_date_start = ""
    patent_date_end = ""
    patent_issued_by = ""
    if employeeInOrg.reasonWorkEmployee == 'P':
        if patent.patentNumber is None or patent == []:
            name_patent_document = ""
            patent_number = ""
            patent_series = ""
            patent_date_start = ""
            patent_date_end = ""
            patent_issued_by = ""
        else:
            name_patent_document = "Патент"
            patent_number = patent.patentNumber
            patent_series = patent.patentSeries
            patent_date_start = patent.dateOfPatentIssue
            patent_date_end = patent.dateExpirationPatent
            patent_issued_by = patent.patentIssuedBy

    # Проверка работает ли сотрудник по ЕАЭС
    eaeu_document = ""
    if employeeInOrg.reasonWorkEmployee == 'EAEU':
        eaeu_document = "Договор ЕАЭС от 29.04.2014"
    else:
        eaeu_document = ""

    # Разделение тексовых данных на элементы
    def split_data(data, count_col):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        for i in range(count_col-count_data_split):
            data_split.append('   ')
        return data_split

    # Получения дня из даты
    def split_day(date):
        if date == "" or date is None:
            day = [" ", " "]
            return day
        else:
            date_split = date.split(".")
            day = list(date_split[0])
            return day

    # Получения месяца из даты
    def split_month(date):
        if date == "" or date is None:
            month = [" ", " "]
            return month
        else:
            date_split = date.split(".")
            month = list(date_split[1])
            return month

    # Получения года из даты
    def split_year(date):
        if date == "" or date is None:
            year = [" ", " ", " ", " "]
            return year
        else:
            date_split = date.split(".")
            year = list(date_split[2])
            return year

    # Разделение данных на несколько строк
    def split_data_rows(data, count_col, number_row):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        length_to_split = [count_col, count_col, count_col]
        output_data = [data_split[x - y: x]
                       for x, y in zip(accumulate(length_to_split), length_to_split)]
        for i in range(len(output_data)):
            if (len(output_data[i]) < count_col):
                for k in range(count_col-len(output_data[i])):
                    output_data[i].append('   ')
        return output_data[number_row-1]

    # Разделение данных на несколько строк с заданным отступом
    def split_data_rows_with_prev(data, prev, count_col, number_row):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        length_to_split = [prev, count_col, count_col]
        output_data = [data_split[x - y: x]
                       for x, y in zip(accumulate(length_to_split), length_to_split)]
        for i in range(len(output_data)):
            if (len(output_data[i]) < count_col):
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
            mark_contract = "V"
            return mark_contract

    context = {
        'mia_name_contents': [
            {'cols': split_data_rows(
                employee.nameMIA, count_col=34, number_row=1)},
            {'cols': split_data_rows(
                employee.nameMIA, count_col=34, number_row=2)},
            {'cols': split_data_rows(
                employee.nameMIA, count_col=34, number_row=3)},
        ],
        'surname_contents': [
            {'cols': split_data(employee.surname, 28)}
        ],
        'name_contents': [
            {'cols': split_data(employee.name, 28)}
        ],
        'patronymic_contents': [
            {'cols': split_data(local_patronymic, 28)}
        ],
        'citizenship_contents': [
            {'cols': split_data(employee.citizenship, 27)}
        ],
        'birthplace_contents': [
            {'cols': split_data_rows(
                employee.birthplace, count_col=24, number_row=1)},
        ],
        'birthplace2_contents': [
            {'cols': split_data_rows_with_prev(
                employee.birthplace, prev=24, count_col=34, number_row=2)},
        ],
        'birthday_contents': [
            {'cols': split_day(defaultfilters.date(
                employee.birthday, 'd.m.Y')) + [" ", ] + split_month(defaultfilters.date(
                    employee.birthday, 'd.m.Y')) + [" ", ] + split_year(defaultfilters.date(
                        employee.birthday, 'd.m.Y'))}
        ],
        'type_identity_document_contents': [
            {'cols': split_data("паспорт", 19)}
        ],
        'series_identity_document_contents': [
            {'cols': split_data(employee.passportSeries, 7)}
        ],
        'number_identity_document_contents': [
            {'cols': split_data(employee.passportNumber, 9)}
        ],
        'identity_document_date_contents': [
            {'cols': split_day(defaultfilters.date(
                employee.passportIssueDate, 'd.m.Y')) + [" ", ] + split_month(defaultfilters.date(employee.passportIssueDate, 'd.m.Y')) + [" ", ] + split_year(defaultfilters.date(employee.passportIssueDate, 'd.m.Y'))}
        ],
        'identity_document_issued_by_contents': [
            {'cols': split_data_rows(
                employee.passportIssuedBy, count_col=28, number_row=1)},
        ],
        'identity_document_issued_by2_contents': [
            {'cols': split_data_rows_with_prev(
                employee.passportIssuedBy, prev=28, count_col=28, number_row=2)},
        ],
        'identity_document_issued_by3_contents': [
            {'cols': split_data_rows_with_prev(
                employee.passportIssuedBy, prev=56, count_col=13, number_row=2)},
        ],
        'name_labor_activity_document_contents': [
            {'cols': split_data_rows(
                eaeu_document, count_col=34, number_row=1)},
            {'cols': split_data_rows(
                eaeu_document, count_col=34, number_row=2)},
            {'cols': split_data_rows(
                eaeu_document, count_col=34, number_row=3)},
        ],

        'name_patent_document_contents': [
            {'cols': split_data(name_patent_document, 21)}
        ],
        'patent_number_contents': [
            {'cols': split_data(patent_number, 10)}
        ],
        'patent_series_contents': [
            {'cols': split_data(patent_series, 7)}
        ],
        'patent_start_date_contents': [{'cols': split_day(defaultfilters.date(
            patent_date_start, 'd.m.Y'))+[" ", ]+split_month(defaultfilters.date(
                patent_date_start, 'd.m.Y'))+[" ", ]+split_year(defaultfilters.date(
                    patent_date_start, 'd.m.Y'))}],
        'patent_end_date_contents': [{'cols': split_day(defaultfilters.date(
            patent_date_end, 'd.m.Y'))+[" ", ]+split_month(defaultfilters.date(
                patent_date_end, 'd.m.Y'))+[" ", ]+split_year(defaultfilters.date(
                    patent_date_end, 'd.m.Y'))}],
        'patent_issued_by_contents': [
            {'cols': split_data_rows(
                patent_issued_by, count_col=27, number_row=1)},
        ],
        'patent_issued_by2_contents': [
            {'cols': split_data_rows_with_prev(
                patent_issued_by, prev=27, count_col=34, number_row=2)},
        ],
        'contract_number_contents': [
            {'cols': contract_check(employeeInOrg.employmentContractNumber)}
        ],
        'contract_gph_number_contents': [
            {'cols': contract_check(employeeInOrg.GPHContractNumber)}
        ],
        'contract_start_date_contents': [{'cols': split_day(defaultfilters.date(
            contract_date, 'd.m.Y'))+[" ", ]+split_month(defaultfilters.date(
                contract_date, 'd.m.Y'))+[" ", ]+split_year(defaultfilters.date(
                    contract_date, 'd.m.Y'))}],

        'legal_organization_address_contents': [
            {'cols': split_data_rows(
                all_address, count_col=34, number_row=1)},
            {'cols': split_data_rows(
                all_address, count_col=34, number_row=2)},
            {'cols': split_data_rows(
                all_address, count_col=34, number_row=3)},
        ],
        'name_profession_contents': [
            {'cols': split_data_rows(
                "Работник пб", count_col=34, number_row=1)},
            {'cols': split_data_rows(
                "Работник пб", count_col=34, number_row=2)},
            {'cols': split_data_rows(
                "Работник пб", count_col=34, number_row=3)},
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
    response["Content-Disposition"] = f"attachment; filename={filename}.docx"
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response

# Уведомление МВД об увольнени


@login_required(login_url='/admin')
def mia_notification_discharge(request, employee_in_org_id):
    # os.path.dirname(employees.__file__)
    doc = DocxTemplate(os.path.join(
        APP_ROOT, "docs", "mia_notification_discharge.docx"))
    # Получение данных из моделей
    employeeInOrg = EmployeeInOrganization.objects.get(
        pk=employee_in_org_id)
    employee = Employee.objects.get(pk=employeeInOrg.employee_id)
    try:
        patent = Patent.objects.get(employee=Employee.objects.get(pk=employeeInOrg.employee_id))
    except Patent.DoesNotExist:
        patent = []

    organization = Organization.objects.get(pk=employeeInOrg.organization_id)

    # Проверка наличия отчества
    if employee.patronymic is None:
        local_patronymic = ""
    else:
        local_patronymic = employee.patronymic

    # Проверка наличия ТД или ГПХ
    contract_date = ' '
    if employeeInOrg.employmentContractNumber == None:
        contract_date = employeeInOrg.startDateOfGPHContract
    else:
        contract_date = employeeInOrg.employmentContractDate

    # Получение полного адреса организация (с индексом)
    all_address = organization.postCodeOrganization + \
        " " + organization.legalOrganizationAddress

    # Получения данных о патенте
    name_patent_document = ""
    patent_number = ""
    patent_series = ""
    patent_date_start = ""
    patent_date_end = ""
    patent_issued_by = ""
    if employeeInOrg.reasonWorkEmployee == 'P':
        if patent.patentNumber is None or patent == []:
            name_patent_document = ""
            patent_number = ""
            patent_series = ""
            patent_date_start = ""
            patent_date_end = ""
            patent_issued_by = ""
        else:
            name_patent_document = "Патент"
            patent_number = patent.patentNumber
            patent_series = patent.patentSeries
            patent_date_start = patent.dateOfPatentIssue
            patent_date_end = patent.dateExpirationPatent
            patent_issued_by = patent.patentIssuedBy

    # Проверка работает ли сотрудник по ЕАЭС
    eaeu_document = ""
    if employeeInOrg.reasonWorkEmployee == 'EAEU':
        eaeu_document = "Договор ЕАЭС от 29.04.2014"
    else:
        eaeu_document = ""

    # Разделение тексовых данных на элементы
    def split_data(data, count_col):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        for i in range(count_col-count_data_split):
            data_split.append('   ')
        return data_split

    # Получения дня из даты
    def split_day(date):
        if date == "" or date is None:
            day = [" ", " "]
            return day
        else:
            date_split = date.split(".")
            day = list(date_split[0])
            return day

    # Получения месяца из даты
    def split_month(date):
        if date == "" or date is None:
            month = [" ", " "]
            return month
        else:
            date_split = date.split(".")
            month = list(date_split[1])
            return month

    # Получения года из даты
    def split_year(date):
        if date == "" or date is None:
            year = [" ", " ", " ", " "]
            return year
        else:
            date_split = date.split(".")
            year = list(date_split[2])
            return year

    # Разделение данных на несколько строк
    def split_data_rows(data, count_col, number_row):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        length_to_split = [count_col, count_col, count_col]
        output_data = [data_split[x - y: x]
                       for x, y in zip(accumulate(length_to_split), length_to_split)]
        for i in range(len(output_data)):
            if (len(output_data[i]) < count_col):
                for k in range(count_col-len(output_data[i])):
                    output_data[i].append('   ')
        return output_data[number_row-1]

    # Разделение данных на несколько строк с заданным отступом
    def split_data_rows_with_prev(data, prev, count_col, number_row):
        data_up = data.upper()
        data_split = list(data_up)
        count_data_split = len(data_split)
        length_to_split = [prev, count_col, count_col]
        output_data = [data_split[x - y: x]
                       for x, y in zip(accumulate(length_to_split), length_to_split)]
        for i in range(len(output_data)):
            if (len(output_data[i]) < count_col):
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
            mark_contract = "V"
            return mark_contract

    context = {
        'mia_name_contents': [
            {'cols': split_data_rows(
                employee.nameMIA, count_col=34, number_row=1)},
            {'cols': split_data_rows(
                employee.nameMIA, count_col=34, number_row=2)},
            {'cols': split_data_rows(
                employee.nameMIA, count_col=34, number_row=3)},
        ],
        'surname_contents': [
            {'cols': split_data(employee.surname, 28)}
        ],
        'name_contents': [
            {'cols': split_data(employee.name, 28)}
        ],
        'patronymic_contents': [
            {'cols': split_data(local_patronymic, 28)}
        ],
        'citizenship_contents': [
            {'cols': split_data(employee.citizenship, 27)}
        ],
        'birthplace_contents': [
            {'cols': split_data_rows(
                employee.birthplace, count_col=24, number_row=1)},
        ],
        'birthplace2_contents': [
            {'cols': split_data_rows_with_prev(
                employee.birthplace, prev=24, count_col=34, number_row=2)},
        ],
        'birthday_contents': [
            {'cols': split_day(defaultfilters.date(
                employee.birthday, 'd.m.Y')) + [" ", ] + split_month(defaultfilters.date(
                    employee.birthday, 'd.m.Y')) + [" ", ] + split_year(defaultfilters.date(
                        employee.birthday, 'd.m.Y'))}
        ],
        'type_identity_document_contents': [
            {'cols': split_data("паспорт", 19)}
        ],
        'series_identity_document_contents': [
            {'cols': split_data(employee.passportSeries, 7)}
        ],
        'number_identity_document_contents': [
            {'cols': split_data(employee.passportNumber, 9)}
        ],
        'identity_document_date_contents': [
            {'cols': split_day(defaultfilters.date(
                employee.passportIssueDate, 'd.m.Y')) + [" ", ] + split_month(defaultfilters.date(employee.passportIssueDate, 'd.m.Y')) + [" ", ] + split_year(defaultfilters.date(employee.passportIssueDate, 'd.m.Y'))}
        ],
        'identity_document_issued_by_contents': [
            {'cols': split_data_rows(
                employee.passportIssuedBy, count_col=28, number_row=1)},
        ],
        'identity_document_issued_by2_contents': [
            {'cols': split_data_rows_with_prev(
                employee.passportIssuedBy, prev=28, count_col=28, number_row=2)},
        ],
        'identity_document_issued_by3_contents': [
            {'cols': split_data_rows_with_prev(
                employee.passportIssuedBy, prev=56, count_col=13, number_row=2)},
        ],
        'name_labor_activity_document_contents': [
            {'cols': split_data_rows(
                eaeu_document, count_col=34, number_row=1)},
            {'cols': split_data_rows(
                eaeu_document, count_col=34, number_row=2)},
            {'cols': split_data_rows(
                eaeu_document, count_col=34, number_row=3)},
        ],

        'name_patent_document_contents': [
            {'cols': split_data(name_patent_document, 21)}
        ],
        'patent_number_contents': [
            {'cols': split_data(patent_number, 10)}
        ],
        'patent_series_contents': [
            {'cols': split_data(patent_series, 7)}
        ],
        'patent_start_date_contents': [{'cols': split_day(defaultfilters.date(
            patent_date_start, 'd.m.Y'))+[" ", ]+split_month(defaultfilters.date(
                patent_date_start, 'd.m.Y'))+[" ", ]+split_year(defaultfilters.date(
                    patent_date_start, 'd.m.Y'))}],
        'patent_end_date_contents': [{'cols': split_day(defaultfilters.date(
            patent_date_end, 'd.m.Y'))+[" ", ]+split_month(defaultfilters.date(
                patent_date_end, 'd.m.Y'))+[" ", ]+split_year(defaultfilters.date(
                    patent_date_end, 'd.m.Y'))}],
        'patent_issued_by_contents': [
            {'cols': split_data_rows(
                patent_issued_by, count_col=27, number_row=1)},
        ],
        'patent_issued_by2_contents': [
            {'cols': split_data_rows_with_prev(
                patent_issued_by, prev=27, count_col=34, number_row=2)},
        ],
        'contract_number_contents': [
            {'cols': contract_check(employeeInOrg.employmentContractNumber)}
        ],
        'contract_gph_number_contents': [
            {'cols': contract_check(employeeInOrg.GPHContractNumber)}
        ],
        'discharge_date_contents': [{'cols': split_day(defaultfilters.date(
            employeeInOrg.dischargeDate, 'd.m.Y'))+[" ", ]+split_month(defaultfilters.date(
                employeeInOrg.dischargeDate, 'd.m.Y'))+[" ", ]+split_year(defaultfilters.date(
                    employeeInOrg.dischargeDate, 'd.m.Y'))}],

        'legal_organization_address_contents': [
            {'cols': split_data_rows(
                all_address, count_col=34, number_row=1)},
            {'cols': split_data_rows(
                all_address, count_col=34, number_row=2)},
            {'cols': split_data_rows(
                all_address, count_col=34, number_row=3)},
        ],
        'name_profession_contents': [
            {'cols': split_data_rows(
                "Работник пб", count_col=34, number_row=1)},
            {'cols': split_data_rows(
                "Работник пб", count_col=34, number_row=2)},
            {'cols': split_data_rows(
                "Работник пб", count_col=34, number_row=3)},
        ],
    }

    doc.render(context)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    response = HttpResponse(doc_io.read())

    now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
    filename = f"Уведомление_МВД_об_увольнении_{employee.fullNameInGenetive}_{now}"
    filename = escape_uri_path(filename)
    response["Content-Disposition"] = f"attachment; filename={filename}.docx"
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response
