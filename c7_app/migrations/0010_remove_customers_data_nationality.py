# Generated by Django 4.2.5 on 2024-12-29 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c7_app', '0009_alter_customers_data_remaining_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers_data',
            name='nationality',
        ),
    ]
