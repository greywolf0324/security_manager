# Generated by Django 4.2.7 on 2024-01-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0048_alter_original_salesimport_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='original_salesimport',
            name='Vendor_Style',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
