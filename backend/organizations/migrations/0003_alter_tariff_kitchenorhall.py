# Generated by Django 3.2.4 on 2021-06-10 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_alter_organization_organizationname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariff',
            name='kitchenOrHall',
            field=models.CharField(choices=[('kitchen', 'Место на кухне'), ('hall', 'Место в зале')], max_length=15, verbose_name='Область работы (кухня, зал)'),
        ),
    ]
