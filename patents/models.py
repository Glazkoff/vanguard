from django.db import models
from employees.models import Employee

class Patent(models.Model):
    """Патент"""
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="ФИО сотрудника")
    dateOfPatentIssue = models.DateField("Дата выдачи патента")
    deleted = models.BooleanField("Удалено", default=False)

    def __str__(self):
        return f"Патент {self.employee.fullNameInGenetive} от {self.dateOfPatentIssue}"

    def delete(self, *args, **kwargs):
        if self.deleted == False:
            self.deleted = True
            self.save()
        else: 
            print('No, man, I have already deleted! Give up!')

    

    class Meta:
        verbose_name = "Патент"
        verbose_name_plural = "Патенты"


class PatentPaymentReceipt(models.Model):
    """Квитанция оплаты патента"""
    patent = models.ForeignKey(
        Patent, on_delete=models.CASCADE, verbose_name="Информация о патенте")
    paymentTermFrom = models.DateField("Срок оплаты патента от")
    paymentTermUntil = models.DateField("Срок оплаты патента до")

    def __str__(self):
        return f'Квитанция об оплате "{self.patent}"'

    class Meta:
        verbose_name = "Квитанция оплаты патента"
        verbose_name_plural = "Квитанции оплаты патентов"
