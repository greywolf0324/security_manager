# Generated by Django 4.2.7 on 2024-01-04 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0010_original_salesimport_approved_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='original_salesimport',
            name='PO_Date',
        ),
    ]
