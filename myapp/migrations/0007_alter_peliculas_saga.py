# Generated by Django 5.1 on 2024-08-22 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_peliculas_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peliculas',
            name='Saga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='peliculas', to='myapp.saga'),
        ),
    ]
