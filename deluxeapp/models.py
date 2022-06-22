from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import User




class Empleado(models.Model):
    Empleado_genero = [
        (1, 'Femenino'),
        (2, 'Masculino')
    ]

    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    genero = models.IntegerField(null=True, blank=False, choices=Empleado_genero)
    edad = models.IntegerField(null=True)
    fechanacimiento = models.DateField(null=True)

    
    def __str__(self):
        return self.nombre

    
class Cargo(models.Model):
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre



class Bus(models.Model):
    placa = models.CharField(max_length=7,unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)

    def __str__(self):
        return self.placa



class Actividad(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    placa = models.CharField(max_length=7)
    fecha = models.DateField()

    def __str__(self):
        return self.id


class Asistencia(models.Model):
    Asistencia_estado = [
        (1, 'Asistencia'),
        (2, 'Inasistencia'),
        (3, 'Por Revisar')
    ]
    Empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    Cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    fecha = models.DateField()
    horaentrada = models.TimeField()
    horasalida = models.TimeField()
    estado = models.IntegerField(null=False, blank=False, choices=Asistencia_estado)


    def __str__(self):
        return str(self.id)