from django.contrib import admin
from .models import Patent, PatentPaymentReceipt
from django.utils.html import format_html
from django.template import defaultfilters
from datetime import date, timedelta
from django.db.models import Max, DateField


class PatentAdmin(admin.ModelAdmin):
    """Патенты"""

    def get_queryset(self, request):
        qs = super(PatentAdmin, self).get_queryset(request)
        qs = qs.annotate(_last_payment_receipt=Max("patentpaymentreceipt__paymentTermUntil", output_field=DateField())).order_by('_last_payment_receipt')
        return qs
    
    def last_payment_receipt(self, obj):
        patentReceiptsQs = PatentPaymentReceipt.objects.filter(
            patent__id=obj.id).order_by('-paymentTermUntil')
        if len(patentReceiptsQs) > 0:
            patentExpirency = patentReceiptsQs[0].paymentTermUntil
            formatPatentExpirency = defaultfilters.date(
                patentExpirency, 'd E Y г.')
            d = date.today()+timedelta(days=14)
            if patentExpirency <= d:
                return format_html('<b style="color:red;">{}</b>', formatPatentExpirency)
            else:
                return format_html('<b>{}</b>', formatPatentExpirency)
        else:
            return "-"
    last_payment_receipt.short_description = "Оплачен до"
    last_payment_receipt.admin_order_field = '_last_payment_receipt'

    list_display = ('employee', 'dateOfPatentIssue', 'last_payment_receipt')

class PatentPaymentReceiptAdmin(admin.ModelAdmin):
    """Квитанция оплаты патента"""
    list_display = ('patent', 'paymentTermFrom', 'paymentTermUntil')


admin.site.register(Patent, PatentAdmin)
admin.site.register(PatentPaymentReceipt, PatentPaymentReceiptAdmin)
