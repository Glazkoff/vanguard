from django.db import models
from django.core.validators import int_list_validator


class Organization(models.Model):
    """Организация"""
    organizationName = models.TextField("Название организации")
    legalOrganizationAddress = models.TextField(
        "Юридический адрес организации")
    cityOrganization = models.TextField(
        "Город организации")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField("Удалено", default=False)


    def __str__(self):
        return self.organizationName

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Tariff(models.Model):
    """Тариф"""
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Название организации")
    positionName = models.CharField("Название должности", max_length=150)
    salaryPerHour = models.PositiveIntegerField("Заработная плата в час", validators=[int_list_validator( sep = '' , message = "ИНН должен содержать только цифры" , code = 'invalid' , allow_negative = False )])
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField("Удалено", default=False)


    def __str__(self):
        return f"{self.positionName} ({self.salaryPerHour}₽ в час)"

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
