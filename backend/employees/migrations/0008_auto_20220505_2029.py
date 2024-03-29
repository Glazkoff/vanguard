# Generated by Django 3.2.13 on 2022-05-05 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20211011_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.CharField(choices=[('AV', 'Авангард'), ('MI', 'Микадо'), ('MP', 'Меркурий Плюс')], default='AV', max_length=2, verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='birthplace',
            field=models.CharField(max_length=120, verbose_name='Место рождения'),
        ),
    ]
