# Generated by Django 3.1.4 on 2021-01-18 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=120, verbose_name='ФИО')),
                ('fullNameInGenetive', models.CharField(max_length=120, verbose_name='Родительный падеж ФИО')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('passportNumber', models.CharField(max_length=40, verbose_name='Номер паспорта')),
                ('passportIssuedBy', models.TextField(verbose_name='Кем выдан паспорт')),
                ('passportValidityPeriod', models.DateField(verbose_name='Срок действия паспорта')),
                ('citizenship', models.CharField(max_length=120, verbose_name='Гражданство')),
                ('phoneNumber', models.CharField(max_length=40, verbose_name='Номер телефона')),
                ('INN', models.CharField(max_length=12, verbose_name='ИНН')),
                ('SNILS', models.CharField(max_length=11, verbose_name='СНИЛС')),
                ('registrationAddress', models.TextField(verbose_name='Адрес регистрации')),
                ('registrationValidityPeriod', models.DateField(verbose_name='Срок действия регистрации')),
                ('dateOfNotificationMVDadmission', models.DateField(verbose_name='Дата уведомления МВД при приёме')),
                ('dateOfNotificationMVDdischarge', models.DateField(verbose_name='Дата уведомления МВД при увольнении')),
                ('bankDetails', models.TextField(verbose_name='Банковские реквизиты')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Работник',
                'verbose_name_plural': 'Работники',
            },
        ),
        migrations.CreateModel(
            name='EmployeeInOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admissionDate', models.DateField(verbose_name='Дата принятия на работу по данному тарифу')),
                ('admissionOrderNumber', models.CharField(max_length=100, verbose_name='Номер приказа о приёме')),
                ('dischargeDate', models.DateField(blank=True, null=True, verbose_name='Дата увольнения')),
                ('dischargeOrderNumber', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер приказа об увольнении')),
                ('employmentContractNumber', models.CharField(max_length=100, verbose_name='Номер трудового договора')),
                ('employmentContractDate', models.DateField(verbose_name='Дата трудового договора')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee', verbose_name='ФИО сотрудника')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization', verbose_name='Название организации')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'Работник в организации',
                'verbose_name_plural': 'Работники в организациях',
            },
        ),
    ]
