# Generated by Django 4.0.4 on 2022-06-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deluxeapp', '0002_alter_bus_placa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]