# Generated by Django 4.0 on 2023-06-30 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0005_remove_monitoringscreen_is_incoming_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]