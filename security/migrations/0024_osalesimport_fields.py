# Generated by Django 4.2.7 on 2024-01-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0023_alter_original_salesimport_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Osalesimport_fields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=50)),
            ],
        ),
    ]