# Generated by Django 3.2.13 on 2022-05-23 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_auto_20220505_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='nameMIA',
            field=models.CharField(blank=True, max_length=240, null=True, verbose_name='Название МВД'),
        ),
    ]
