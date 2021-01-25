from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models import Patent, PatentPaymentReceipt
from django.utils.html import format_html
from django.template import defaultfilters
from datetime import date, timedelta
from django.db.models import Max, DateField

class PatentPaymentReceiptInline(admin.TabularInline):
    """Квитанции об оплате патентов"""
    model = PatentPaymentReceipt
    extra = 1

class PatentResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта патентов"""
    class Meta:
        model = Patent

class PatentAdmin(ImportExportModelAdmin):
    """Патенты"""
    search_fields=('employee__fullName', 'dateOfPatentIssue', 'patentpaymentreceipt__paymentTermUntil')
    inlines = [PatentPaymentReceiptInline]
    # Поиск по дате выдачи патента и даты оплаты "до" пока осуществляется в формате YYYY-MM-dd
    resource_class = PatentResource
    actions = ["makeDeleted",]

    def get_queryset(self, request):
            qs = super(PatentAdmin, self).get_queryset(request)
            qs = qs.filter(deleted=False).annotate(_last_payment_receipt=Max(
                "patentpaymentreceipt__paymentTermUntil", output_field=DateField())).order_by('_last_payment_receipt')
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

    def makeDeleted(self, request, queryset):
        row_update = queryset.update(deleted=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    makeDeleted.short_description = "Удалить выбранные патенты"
    makeDeleted.allowed_permissions = ('delete', )

    last_payment_receipt.short_description = "Оплачен до"
    last_payment_receipt.admin_order_field = '_last_payment_receipt'
    list_display = ('employee', 'dateOfPatentIssue', 'last_payment_receipt')

class PatentPaymentReceiptResource(resources.ModelResource): 
    """Ресурс для импорта-экспорта квитанций об оплате патентов"""
    class Meta:
        model = PatentPaymentReceipt

class PatentPaymentReceiptAdmin(ImportExportModelAdmin):
    """Квитанция оплаты патента"""
    list_display = ('patent', 'paymentTermFrom', 'paymentTermUntil')
    search_fields=('patent__employee__fullName', 'patent__dateOfPatentIssue','paymentTermFrom', 'paymentTermUntil')
    resource_class = PatentPaymentReceiptResource

admin.site.register(Patent, PatentAdmin)
admin.site.register(PatentPaymentReceipt, PatentPaymentReceiptAdmin)
