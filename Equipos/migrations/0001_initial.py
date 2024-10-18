# Generated by Django 5.1.1 on 2024-09-13 15:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
                ('descripcion', models.TextField(blank=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoAlerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoHardware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
                ('estado', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Equipos.area')),
                ('estado_alerta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Equipos.estadoalerta')),
                ('estado_equipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Equipos.estadoequipo')),
            ],
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disk', to='Equipos.equipo')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Equipos.estadohardware')),
            ],
        ),
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu', to='Equipos.equipo')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Equipos.estadohardware')),
            ],
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory', to='Equipos.equipo')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Equipos.estadohardware')),
            ],
        ),
    ]