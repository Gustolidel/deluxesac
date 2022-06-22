
from django.contrib import admin
from .models import Bus, Empleado, Asistencia, Cargo, Actividad
# Register your models here.
admin.site.register(Bus)
admin.site.register(Asistencia)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Actividad)