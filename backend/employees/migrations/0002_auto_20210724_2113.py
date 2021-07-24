# Generated by Django 3.2.5 on 2021-07-24 18:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='passportSeries',
            field=models.CharField(blank=True, default='', max_length=40, verbose_name='Серия паспорта'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='patronymic',
            field=models.CharField(blank=True, default='', max_length=40, validators=[django.core.validators.RegexValidator(code=None, flags=0, inverse_match=None, message='Отчество может содержать только буквы или дефис', regex='^[a-zA-Zа-яА-ЯёЁ -]+$')], verbose_name='Отчество'),
        ),
    ]