# Generated by Django 3.1 on 2020-10-09 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_auto_20201008_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of Payment'),
        ),
    ]
