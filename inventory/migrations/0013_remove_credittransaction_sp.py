# Generated by Django 3.0.7 on 2020-10-01 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20201001_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credittransaction',
            name='sp',
        ),
    ]
