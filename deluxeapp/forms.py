from django import forms
from django.forms import widgets
from .models import Bus,Empleado,Cargo,Asistencia,Actividad
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput, TextInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })



class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['placa', 'modelo', 'marca']
        



class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'genero', 'edad', 'fechanacimiento']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['genero'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['edad'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['fechanacimiento'].widget.attrs.update({
            'class': 'form-control',
        })
        


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre']

    def clean_cargo(self):
        nombre = self.cleaned_data['nombre']
        if not nombre:
            return nombre

        if not nombre[0].isupper():
            self.add_error('nombre', 'Should start with an uppercase letter')
        return nombre


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['empleado', 'fecha', 'placa']


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['Empleado', 'Cargo', 'fecha', 'horaentrada', 'horasalida', 'estado']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['Empleado'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['Cargo'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['fecha'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['horaentrada'].widget.attrs.update({
            'class': 'form-control',
        })    
        self.fields['horasalida'].widget.attrs.update({
            'class': 'form-control',
        })    
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control',
        })    