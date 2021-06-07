from django.db import models
from employees.models import Employee
from django.core.exceptions import ValidationError

class Patent(models.Model):
    """Патент"""
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="ФИО сотрудника")
    dateOfPatentIssue = models.DateField("Дата выдачи патента")
    dateExpirationPatent = models.DateField("Дата окончания патента")
    patentSeries = models.CharField("Серия патента", max_length=15)
    patentNumber = models.CharField("Номер патента", max_length=12)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"Патент {self.employee.fullNameInGenetive} от {self.dateOfPatentIssue}"

    class Meta:
        verbose_name = "Патент"
        verbose_name_plural = "Патенты"


class PatentPaymentReceipt(models.Model):
    """Квитанция оплаты патента"""
    patent = models.ForeignKey(
        Patent, on_delete=models.CASCADE, verbose_name="Информация о патенте")
    paymentTermFrom = models.DateField("Срок оплаты патента от")
    paymentTermUntil = models.DateField("Срок оплаты патента до")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Квитанция об оплате "{self.patent}"'

    class Meta:
        verbose_name = "Квитанция оплаты патента"
        verbose_name_plural = "Квитанции оплаты патентов"

    def clean(self):
        if self.paymentTermFrom > self.paymentTermUntil:
            raise ValidationError("Начало срока оплаты патента превышает его окончание")
