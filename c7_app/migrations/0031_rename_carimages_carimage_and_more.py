# Generated by Django 4.2.5 on 2025-04-26 23:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('c7_app', '0030_historicalcar'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarImages',
            new_name='CarImage',
        ),
        migrations.RenameModel(
            old_name='customers_data',
            new_name='CustomersData',
        ),
    ]
