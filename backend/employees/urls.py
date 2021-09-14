from employees.views import labor_contract, gph_contract, mia_notifications_admission,mia_notification_discharge
from django.urls import path

urlpatterns = [
#     path('documents/', doc_test),
#     path('documents_m/', doc_multiple_test),
    path('documents/labor_contract/<int:employee_in_org_id>/', labor_contract),
    path('documents/gph_contract/<int:employee_in_org_id>/', gph_contract),
    path('documents/mia_notifications_admission/<int:employee_in_org_id>/',
         mia_notifications_admission),
    path('documents/mia_notification_discharge/<int:employee_in_org_id>/',
         mia_notification_discharge)
]
