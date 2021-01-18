from django.db import models


class Organization(models.Model):
    """Организация"""
    organizationName = models.TextField("Название организации")
    legalOrganizationAddress = models.TextField(
        "Юридический адрес организации")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

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
    salaryPerHour = models.PositiveIntegerField("Заработная плата в час")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.positionName} ({self.salaryPerHour}₽ в час)"

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
