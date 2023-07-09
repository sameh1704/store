# Generated by Django 4.0 on 2023-06-30 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0008_remove_room_floor_number_building_rooms_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='building',
        ),
        migrations.AlterField(
            model_name='building',
            name='rooms',
            field=models.ManyToManyField(to='Inventory.Room'),
        ),
    ]
