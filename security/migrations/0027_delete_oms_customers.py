# Generated by Django 4.2.7 on 2024-01-05 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0026_alter_oms_customers_accountreceivable_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OMS_Customers',
        ),
    ]