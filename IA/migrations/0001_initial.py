# Generated by Django 5.1.1 on 2024-10-17 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Equipos', '0008_alter_equipo_modelo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeloIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('archivo', models.FileField(upload_to='modelos/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('modelo_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Equipos.modelo')),
            ],
        ),
    ]
