# Generated by Django 4.2.7 on 2024-01-05 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0021_original_salesimport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='original_salesimport',
            name='created',
            field=models.CharField(max_length=30, null=True),
        ),
    ]