# Generated by Django 3.0.7 on 2020-10-01 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_debittransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='debittransaction',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
        ),
        migrations.AddField(
            model_name='debittransaction',
            name='remarks',
            field=models.TextField(blank=True, null=True, verbose_name='Remarks on Deal'),
        ),
    ]
