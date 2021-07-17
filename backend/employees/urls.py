from django.urls import path
from employees.views import doc_test, doc_multiple_test, labor_contract, mia_notifications_admission

urlpatterns = [
    path('documents/', doc_test),
    path('documents_m/', doc_multiple_test),
    path('documents/labor_contract/<int:employee_in_org_id>/', labor_contract),
    path('documents/mia_notifications_admission', mia_notifications_admission)
]
