# Generated by Django 4.2.7 on 2024-01-05 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0031_delete_oms_additionaluom'),
    ]

    operations = [
        migrations.CreateModel(
            name='OMS_AdditionalUOM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Action', models.CharField(max_length=100, null=True)),
                ('BaseSKU', models.CharField(max_length=100, null=True)),
                ('BaseProductName', models.CharField(max_length=100, null=True)),
                ('BaseUnitsOfMeasure', models.CharField(max_length=100, null=True)),
                ('AdditionalUnitsOfMeasureSKU', models.CharField(max_length=100, null=True)),
                ('AdditionalUnitsOfMeasureProductName', models.CharField(max_length=100, null=True)),
                ('AdditionalUnitsOfMeasureName', models.CharField(max_length=100, null=True)),
                ('NumberOfBaseUnitsInAdditionalUnit', models.IntegerField(null=True)),
                ('IAmSellingThisProduct', models.BooleanField()),
            ],
        ),
    ]
