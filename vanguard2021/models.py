from django.db import models

class Employee(models.Model):
    """Работники"""
    fullName = models.CharField("ФИО", max_length=120)
    fullNameInGenetive = models.CharField("Родительный падеж ФИО", max_length=120)
    birthday = models.DateField("Дата рождения")
    passportNumber = models.CharField("Номер паспорта", max_length=40)
    passportIssuedBy = models.TextField("Кем выдан паспорт")
    passportValidityPeriod = models.DateField("Срок действия паспорта")
    citizenship = models.CharField("Гражданство", max_length=120)
    phoneNumber = models.CharField("Номер телефона", max_length=40)
    INN = models.CharField("ИНН", max_length=12)
    SNILS = models.CharField("СНИЛС", max_length=11)
    registrationAddress = models.TextField("Адрес регистрации")
    registrationValidityPeriod = models.DateField("Срок действия регистрации")
    dateOfNotificationMVDadmission = models.DateField("Дата уведомления МВД при приёме")
    dateOfNotificationMVDdischarge = models.DateField("Дата уведомления МВД при увольнении")
    bankDetails = models.TextField("Банковские реквизиты")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.fullName

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

class Organization(models.Model):
    """Организация"""
    organizationName = models.TextField("Название организации")
    legalOrganizationAddress = models.TextField("Юридический адрес организации")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.organizationName

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

class Tariff(models.Model):
    """Тариф"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Название организации")
    positionName = models.CharField("Название должности", max_length=150)
    salaryPerHour = models.PositiveIntegerField("Заработная плата в час")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"{self.positionName} ({self.salaryPerHour}₽ в час)"


    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

class EmployeeInOrganization(models.Model):
    """Сотрудник в организации"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="ФИО сотрудника")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Название организации")
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name="Тариф")
    admissionDate = models.DateField("Дата принятия на работу по данному тарифу")
    admissionOrderNumber = models.CharField("Номер приказа о приёме", max_length=100)
    dischargeDate = models.DateField("Дата увольнения", null=True, blank=True)
    dischargeOrderNumber = models.CharField("Номер приказа об увольнении", max_length=100, null=True, blank=True)
    employmentContractNumber = models.CharField("Номер трудового договора", max_length=100)
    employmentContractDate = models.DateField("Дата трудового договора")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"Работа {self.employee.fullNameInGenetive} в {self.organization.organizationName} по должности {self.tariff.positionName} ({self.tariff.salaryPerHour}₽ в час)"

    class Meta:
        verbose_name = "Работник в организации"
        verbose_name_plural = "Работники в организациях"

class Patent(models.Model):
    """Патент"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="ФИО сотрудника")
    dateOfPatentIssue = models.DateField("Дата выдачи патента")
    def __str__(self):
        return f"Патент {self.employee.fullNameInGenetive} от {self.dateOfPatentIssue}"

    class Meta:
        verbose_name = "Патент"
        verbose_name_plural = "Патенты"


class PatentPaymentReceipt(models.Model):
    """Квитанция оплаты патента"""
    patent = models.ForeignKey(Patent, on_delete=models.CASCADE, verbose_name="Информация о патенте")
    paymentTermFrom = models.DateField("Срок оплаты патента от")
    paymentTermUntil = models.DateField("Срок оплаты патента до")
    
    def __str__(self):
        return f'Квитанция об оплате "{self.patent}"'

    class Meta:
        verbose_name = "Квитанция оплаты патента"
        verbose_name_plural = "Квитанции оплаты патентов"