from django.db import models
from django.core.validators import int_list_validator

class City(models.Model):
    """Город"""
    cityName = models.TextField("Название города")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cityName

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Organization(models.Model):
    """Организация"""
    organizationName = models.TextField("Название организации")
    legalOrganizationAddress = models.TextField(
        "Юридический адрес организации")
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name="Город организации")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.organizationName

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Tariff(models.Model):
    """Тариф"""
    PLACE_CHOICES = (('kitchen', 'Место на кухне'),('hall', 'Место в зале'))
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name="Город организации")

    positionName = models.CharField("Название должности", max_length=150)
    salaryPerHour = models.PositiveIntegerField("Заработная плата в час", validators=[int_list_validator( sep = '' , message = "ИНН должен содержать только цифры" , code = 'invalid' , allow_negative = False )])
    kitchenOrHall = models.CharField("Область работы (кухня, зал)", max_length=15, choices=PLACE_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.positionName} ({self.salaryPerHour}₽ в час)"

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
