# Generated by Django 5.1.1 on 2024-11-15 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress_info',
            name='shipping_address2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress_info',
            name='shipping_state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress_info',
            name='shipping_zipcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]