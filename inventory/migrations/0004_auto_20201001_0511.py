# Generated by Django 3.0.7 on 2020-10-01 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20200929_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Available Quantity'),
        ),
    ]
