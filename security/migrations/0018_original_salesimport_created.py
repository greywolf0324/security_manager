# Generated by Django 4.2.7 on 2024-01-05 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0017_alter_original_salesimport_pack_size_uom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='original_salesimport',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]