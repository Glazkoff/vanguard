# Generated by Django 3.2.3 on 2021-05-31 17:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizationName', models.TextField(verbose_name='Название организации')),
                ('legalOrganizationAddress', models.TextField(verbose_name='Юридический адрес организации')),
                ('cityOrganization', models.TextField(verbose_name='Город организации')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positionName', models.CharField(max_length=150, verbose_name='Название должности')),
                ('salaryPerHour', models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\d+)*\\Z'), code='invalid', message='ИНН должен содержать только цифры')], verbose_name='Заработная плата в час')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization', verbose_name='Название организации')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
    ]
