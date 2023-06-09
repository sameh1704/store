# Generated by Django 4.0 on 2023-06-30 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0007_remove_building_rooms_room_building_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='floor_number',
        ),
        migrations.AddField(
            model_name='building',
            name='rooms',
            field=models.ManyToManyField(related_name='building_rooms', to='Inventory.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_building', to='Inventory.building'),
        ),
    ]
