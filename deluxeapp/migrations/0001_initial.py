# Generated by Django 4.0.4 on 2022-06-26 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=7, unique=True)),
                ('modelo', models.CharField(max_length=50)),
                ('marca', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('genero', models.IntegerField(choices=[(1, 'Femenino'), (2, 'Masculino')], null=True)),
                ('edad', models.IntegerField(null=True)),
                ('fechanacimiento', models.DateField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('horaentrada', models.TimeField()),
                ('horasalida', models.TimeField()),
                ('estado', models.IntegerField(choices=[(1, 'Asistencia'), (2, 'Inasistencia'), (3, 'Por Revisar')])),
                ('Cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deluxeapp.cargo')),
                ('Empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deluxeapp.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=7)),
                ('fecha', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deluxeapp.empleado')),
            ],
        ),
    ]
