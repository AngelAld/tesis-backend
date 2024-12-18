# Generated by Django 5.1.1 on 2024-09-13 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Equipos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='equipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu_set', to='Equipos.equipo'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='equipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disk_set', to='Equipos.equipo'),
        ),
        migrations.AlterField(
            model_name='memory',
            name='equipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory_set', to='Equipos.equipo'),
        ),
    ]
