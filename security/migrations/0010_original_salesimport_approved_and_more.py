# Generated by Django 4.2.7 on 2024-01-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0009_alter_original_salesimport_po_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='original_salesimport',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='original_salesimport',
            name='start_line',
            field=models.BooleanField(default=False),
        ),
    ]
