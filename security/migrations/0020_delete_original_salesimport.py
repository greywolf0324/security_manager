# Generated by Django 4.2.7 on 2024-01-05 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0019_remove_original_salesimport_additional_vendor_part_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Original_SalesImport',
        ),
    ]
