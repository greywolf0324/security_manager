# Generated by Django 4.2.7 on 2024-01-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0025_oms_additionaluom_oms_customers_oms_inventory_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oms_customers',
            name='AccountReceivable',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Carrier',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='ContactComment',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='ContactDefault',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='ContactIncludeInEmail',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='CreditLimit',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Currency',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Discount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Fax',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='IsAccountingDimensionEnabled',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='MarketingConsent',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='MobilePhone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='PaymentTerm',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='PriceTier',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='SaleAccount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='SalesRepresentative',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='TaxNumber',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='TaxRule',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='oms_customers',
            name='Website',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
