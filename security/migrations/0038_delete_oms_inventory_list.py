# Generated by Django 4.2.7 on 2024-01-05 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0037_alter_oms_additionaluom_iamsellingthisproduct_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OMS_Inventory_List',
        ),
    ]