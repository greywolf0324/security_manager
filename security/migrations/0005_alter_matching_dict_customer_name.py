# Generated by Django 4.2.7 on 2024-01-04 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0004_customers_matching_dict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matching_dict',
            name='customer_name',
            field=models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='security.customers'),
        ),
    ]
