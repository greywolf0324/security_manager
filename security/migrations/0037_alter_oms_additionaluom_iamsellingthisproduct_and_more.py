# Generated by Django 4.2.7 on 2024-01-05 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0036_oms_inventory_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oms_additionaluom',
            name='IAmSellingThisProduct',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_inventory_list',
            name='IsAccountingDimensionEnabled',
            field=models.BooleanField(null=True),
        ),
    ]
