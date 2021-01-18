from django.contrib import admin
from .models import Patent, PatentPaymentReceipt


class PatentAdmin(admin.ModelAdmin):
    """Патенты"""
    list_display = ('employee', 'dateOfPatentIssue')


class PatentPaymentReceiptAdmin(admin.ModelAdmin):
    """Квитанция оплаты патента"""
    list_display = ('patent', 'paymentTermFrom', 'paymentTermUntil')


admin.site.register(Patent, PatentAdmin)
admin.site.register(PatentPaymentReceipt, PatentPaymentReceiptAdmin)
