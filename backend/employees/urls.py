from django.urls import path
from employees.views import doc_test, doc_multiple_test, labor_contract, gph_contract

urlpatterns = [
    path('documents/', doc_test),
    path('documents_m/', doc_multiple_test),
    path('documents/labor_contract/<int:employee_in_org_id>/', labor_contract),
    path('documents/gph_contract/<int:employee_in_org_id>/', gph_contract)

]
