from django.db import models

# Create your models here.
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
    registrationValidityPeriod = models.DateTimeField("Срок действия регистрации")
    dateOfNotificationMVDadmission = models.DateTimeField("Дата уведомления МВД при приёме")
    dateOfNotificationMVDdischarge = models.DateTimeField("Дата уведомления МВД при увольнении")
    bankDetails = models.TextField("Банковские реквизиты")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.fullName

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"