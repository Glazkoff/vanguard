from patents.models import PatentPaymentReceipt, Patent
from datetime import date, timedelta
from django.utils.html import format_html
from django.template import defaultfilters


def go_through_patents():
    notifications = []
    patents = Patent.objects.all()
    for patent in patents:
        patentReceiptsQs = PatentPaymentReceipt.objects.filter(
            patent__id=patent.id).order_by('-paymentTermUntil')
        if len(patentReceiptsQs) > 0:
            patentExpirency = patentReceiptsQs[0].paymentTermUntil
            formatPatentExpirency = defaultfilters.date(
                patentExpirency, 'd E Y г.')
            d = date.today()+timedelta(days=14)
            if patentExpirency <= d:
                _ = patent.employee
                notifications.append('<a href="/admin/patents/patent/'+str(patent.id)+'/change/">Патент #'+str(
                    _.id)+'</a> сотрудника <a href="/admin/employees/employee/'+str(_.id)+'/change/">'+_.fullNameInGenetive+'</a> оплачен только до '+formatPatentExpirency+"!")
    return notifications


def context_processor(request):
    extra_context = {}
    if request.path == '/admin/':
        extra_context['notifications'] = go_through_patents()
    return extra_context
