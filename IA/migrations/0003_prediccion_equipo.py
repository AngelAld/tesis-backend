# Generated by Django 5.1.1 on 2024-10-18 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Equipos', '0008_alter_equipo_modelo'),
        ('IA', '0002_modeloia_variable_objetivo_prediccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediccion',
            name='equipo',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='Equipos.equipo'),
            preserve_default=False,
        ),
    ]
