# Generated by Django 3.2.4 on 2021-06-10 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organizationName',
            field=models.CharField(max_length=150, verbose_name='Название организации'),
        ),
    ]
