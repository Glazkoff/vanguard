from django.db import models
from organizations.models import Organization, Tariff
from django.core.validators import MaxLengthValidator, MinLengthValidator, int_list_validator, MaxValueValidator, RegexValidator
from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    """Работники"""
    fullName = models.CharField("ФИО", max_length=120, validators=[RegexValidator( regex=r'^[a-zA-Zа-яА-ЯёЁ -]+$', message = "ФИО должно содержать только буквы" , code = None , inverse_match = None , flags = 0 )])
    fullNameInGenetive = models.CharField(
        "Родительный падеж ФИО", max_length=120, validators=[RegexValidator( regex=r'^[a-zA-Zа-яА-ЯёЁ -]+$', message = "ФИО должно содержать только буквы" , code = None , inverse_match = None , flags = 0 )])
    birthday = models.DateField("Дата рождения", validators=[MaxValueValidator(limit_value=date.today, message = "Дата рождения не может превышать сегодняшнюю")])
    passportNumber = models.CharField("Номер паспорта", max_length=40, validators=[int_list_validator( sep = ' ' , message = "Неправильный вид номера паспорта" , code = 'invalid' , allow_negative = False )])
    passportIssuedBy = models.TextField("Кем выдан паспорт")
    passportValidityPeriod = models.DateField("Срок действия паспорта")
    citizenship = models.CharField("Гражданство", max_length=120, validators=[RegexValidator( regex=r'^[a-zA-Zа-яА-ЯёЁ ]+$', message = "Название страны содержить только буквы" , code = None , inverse_match = None , flags = 0 )])
    phoneNumber = models.CharField("Номер телефона", max_length=40)
    INN = models.CharField("ИНН", max_length=12, validators=[MinLengthValidator(limit_value=12, message="ИНН не может состоят из менее чем 12 цифр"), int_list_validator( sep = '' , message = "ИНН должен содержать только цифры" , code = 'invalid' , allow_negative = False )])
    SNILS = models.CharField("СНИЛС", max_length=11, validators=[MinLengthValidator(limit_value=11, message="СНИЛС не может состоят из менее чем 11 цифр"), int_list_validator( sep = '' , message = "СНИЛС должен содержать только цифры" , code = 'invalid' , allow_negative = False )])
    registrationAddress = models.TextField("Адрес регистрации")
    registrationValidityPeriod = models.DateField("Срок действия регистрации")
    dateOfNotificationMVDadmission = models.DateField(
        "Дата уведомления МВД при приёме")
    dateOfNotificationMVDdischarge = models.DateField(
        "Дата уведомления МВД при увольнении")
    bankDetails = models.TextField("Банковские реквизиты")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField("Удалено", default=False)


    def __str__(self):
        return self.fullName

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def clean(self):
        if self.dateOfNotificationMVDadmission > self.dateOfNotificationMVDdischarge:
            raise ValidationError("Дата уведомления о приеме превышает даты при увольнении")


class EmployeeInOrganization(models.Model):
    """Сотрудник в организации"""
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="ФИО сотрудника")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Название организации")
    tariff = models.ForeignKey(
        Tariff, on_delete=models.CASCADE, verbose_name="Тариф")
    admissionDate = models.DateField(
        "Дата принятия на работу по данному тарифу")
    admissionOrderNumber = models.CharField(
        "Номер приказа о приёме", max_length=100)
    dischargeDate = models.DateField("Дата увольнения", null=True, blank=True)
    dischargeOrderNumber = models.CharField(
        "Номер приказа об увольнении", max_length=100, null=True, blank=True)
    employmentContractNumber = models.CharField(
        "Номер трудового договора", max_length=100)
    employmentContractDate = models.DateField("Дата трудового договора")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Работа {self.employee.fullNameInGenetive} в {self.organization.organizationName} по должности {self.tariff.positionName} ({self.tariff.salaryPerHour}₽ в час)"

    class Meta:
        verbose_name = "Работник в организации"
        verbose_name_plural = "Работники в организациях"