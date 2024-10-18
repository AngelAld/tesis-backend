# Generated by Django 5.1.1 on 2024-10-07 19:07

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
    ]
