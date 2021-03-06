# Generated by Django 3.1 on 2020-10-03 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20201003_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='vendor_client',
            field=models.CharField(default='a', max_length=240, verbose_name='Vendor or Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cost',
            field=models.IntegerField(default=0, verbose_name='Cost Price Per Quantity Unit'),
        ),
    ]
