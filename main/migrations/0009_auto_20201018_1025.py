# Generated by Django 3.1 on 2020-10-18 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20201018_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutdata',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='checkoutdata',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to='main.order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='checkoutdata',
            name='remarks',
            field=models.TextField(blank=True, null=True, verbose_name='Remarks'),
        ),
    ]