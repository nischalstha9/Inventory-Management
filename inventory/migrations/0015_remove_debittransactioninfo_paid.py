# Generated by Django 3.0.7 on 2020-10-02 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20201002_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debittransactioninfo',
            name='paid',
        ),
    ]
