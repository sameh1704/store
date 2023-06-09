# Generated by Django 4.0 on 2023-06-19 10:30

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_rename_building_outgoing_building_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcode',
            name='incoming',
        ),
        migrations.DeleteModel(
            name='Printer',
        ),
        migrations.RenameField(
            model_name='inventoryreport',
            old_name='Product_Category',
            new_name='product_category',
        ),
        migrations.RenameField(
            model_name='monitoringscreen',
            old_name='Product_Category',
            new_name='product_category',
        ),
        migrations.RemoveField(
            model_name='room',
            name='Building',
        ),
        migrations.AddField(
            model_name='building',
            name='rooms',
            field=models.ManyToManyField(to='Inventory.Room'),
        ),
        migrations.AlterField(
            model_name='product_category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
        migrations.DeleteModel(
            name='Barcode',
        ),
    ]
