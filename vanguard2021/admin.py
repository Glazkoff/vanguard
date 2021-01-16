from django.contrib import admin

from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Работники"""
    list_display = ("fullName", "fullNameInGenetive","birthday","passportNumber","passportIssuedBy","passportValidityPeriod","citizenship","phoneNumber","INN","SNILS","registrationAddress","registrationValidityPeriod","dateOfNotificationMVDadmission","dateOfNotificationMVDdischarge","bankDetails")