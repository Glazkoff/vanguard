from employees.views import labor_contract, gph_contract_avangard, gph_contract_mercury, gph_contract_mikado, mia_notifications_admission,mia_notification_discharge, cover_letter_avangard, cover_letter_mikado, cover_letter_mercury
from django.urls import path

urlpatterns = [
    #     path('documents/', doc_test),
    #     path('documents_m/', doc_multiple_test),
    path('documents/cover_letter/avangard/<int:employee_in_org_id>/',
         cover_letter_avangard),
    path('documents/cover_letter/mikado/<int:employee_in_org_id>/',
         cover_letter_mikado),
    path('documents/cover_letter/mercury/<int:employee_in_org_id>/',
         cover_letter_mercury),
    path('documents/labor_contract/<int:employee_in_org_id>/', labor_contract),
    path('documents/gph_contract_avangard/<int:employee_in_org_id>/', gph_contract_avangard),
    path('documents/gph_contract_mercury/<int:employee_in_org_id>/', gph_contract_mercury),
    path('documents/gph_contract_mikado/<int:employee_in_org_id>/', gph_contract_mikado),
    path('documents/mia_notifications_admission/<int:employee_in_org_id>/',
         mia_notifications_admission),
    path('documents/mia_notification_discharge/<int:employee_in_org_id>/',
         mia_notification_discharge)
]
