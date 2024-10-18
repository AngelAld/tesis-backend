# Generated by Django 5.1.1 on 2024-10-07 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Areas', '0001_initial'),
        ('Equipos', '0005_remove_equipo_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='area',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='Areas.area'),
            preserve_default=False,
        ),
    ]
