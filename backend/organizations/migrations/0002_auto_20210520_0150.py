# Generated by Django 3.2.3 on 2021-05-19 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
        migrations.AddField(
            model_name='tariff',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
    ]
