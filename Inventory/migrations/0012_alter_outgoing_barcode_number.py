# Generated by Django 4.0 on 2023-06-30 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0011_remove_outgoing_barcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgoing',
            name='barcode_number',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
