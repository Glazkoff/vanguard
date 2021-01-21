from django.contrib import admin
from .models import Patent, PatentPaymentReceipt
from django.utils.html import format_html
from django.template import defaultfilters
from datetime import date, timedelta

class PatentPaymentReceiptInline(admin.TabularInline):
    model = PatentPaymentReceipt
    extra = 1

class PatentAdmin(admin.ModelAdmin):
    """Патенты"""
    list_display = ('employee', 'dateOfPatentIssue', 'last_payment_receipt')
    search_fields=('employee__fullName', 'dateOfPatentIssue', 'patentpaymentreceipt__paymentTermUntil')
    inlines = [PatentPaymentReceiptInline]
    # Поиск по дате выдачи патента и даты оплаты "до" пока осуществляется в формате YYYY-MM-dd

    def last_payment_receipt(self, obj):
        patentReceiptsQs = PatentPaymentReceipt.objects.filter(
            patent__id=obj.id).order_by('-paymentTermUntil')
        if len(patentReceiptsQs) > 0:
            patentExpirency = patentReceiptsQs[0].paymentTermUntil
            formatPatentExpirency = defaultfilters.date(
                patentExpirency, 'd E Y г.')
            d = date.today()+timedelta(days=14)
            if patentExpirency < d:
                return format_html('<b style="color:red;">{}</b>', formatPatentExpirency)
            else:
                return format_html('<b>{}</b>', formatPatentExpirency)
        else:
            return "-"
    last_payment_receipt.short_description = "Оплачен до"
    last_payment_receipt.admin_order_field = 'patentPaymentReceipt'


class PatentPaymentReceiptAdmin(admin.ModelAdmin):
    """Квитанция оплаты патента"""
    list_display = ('patent', 'paymentTermFrom', 'paymentTermUntil')
    search_fields=('patent__employee__fullName', 'patent__dateOfPatentIssue','paymentTermFrom', 'paymentTermUntil')


admin.site.register(Patent, PatentAdmin)
admin.site.register(PatentPaymentReceipt, PatentPaymentReceiptAdmin)
