# Generated by Django 5.1.1 on 2024-11-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IA', '0003_prediccion_equipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeloia',
            name='componente',
            field=models.CharField(default='cpu', max_length=100),
            preserve_default=False,
        ),
    ]
