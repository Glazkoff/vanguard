# Generated by Django 3.2.8 on 2021-10-11 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20211006_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_city',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_country',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_home',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_home_expansion',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_locality',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_street',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='birthplace_subject',
        ),
        migrations.AddField(
            model_name='employee',
            name='birthplace',
            field=models.CharField(blank=True, max_length=120, verbose_name='Место рождения'),
        ),
    ]
