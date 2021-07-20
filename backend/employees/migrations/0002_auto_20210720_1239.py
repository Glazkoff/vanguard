# Generated by Django 3.2.5 on 2021-07-20 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='bankDetailsCardNumber',
            field=models.CharField(blank=True, default='', max_length=16, verbose_name='Номер банковской карты'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='passportNumber',
            field=models.CharField(max_length=40, verbose_name='Номер паспорта'),
        ),
    ]
