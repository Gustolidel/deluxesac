import pytest
from django.test import Client
from urllib import request, response
from django.test import TestCase
from django.http import HttpRequest
from deluxeapp.models import Asistencia, Bus, Cargo, Empleado
from deluxeapp.forms import BusForm, CargoForm, CreateUserForm, AsistenciaForm
from django.contrib.auth.models import User
#from deluxeapp.views import createCargo


#el codigo verificará que el campo username esté ingresado 
class TestUserForm(TestCase):
    def test_user(self):
        user = User.objects.create_user(
            username = "gakdo",
            email = "gakdo@gmail.com",
            password = "luisallcca",
            is_active = True,
            is_staff = False
        )

        assert user.username == "gakdo" and user.email == "gakdo@gmail.com" and user.is_staff == False

        
#valida que el dato del form sea valido y no este vacio
class AddCargoFormTests(TestCase):
    def test_CargoForm(self):
        form_data = {'nombre':'Estudiante'}
        form = CargoForm(data=form_data)
        self.assertTrue(form.is_valid())


#cumple con los criterios de formulario (campos vacios, limite)
class AddBusFormTests(TestCase):
    def test_BusForm(self):
        form_data = {'placa':'dc6-456','modelo':'yaris','marca':'toyota'}
        form = BusForm(data=form_data)
        self.assertTrue(form.is_valid())




#se prueba que los datos ingresados 
class TestBusForm(TestCase):
    def setUp(self):
        self.bus = Bus.objects.create(placa="345354", modelo="yaris", marca="toyota")


class Bus_Form_Test(TestCase):

    def test_UserForm_valid(self):
        form=BusForm(data={'placa': '345354', 'modelo': 'yaris', 'marca':'toyota'})
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):
        form=BusForm(data={'placa':'', 'modelo':'mp','marca':''})
        self.assertFalse(form.is_valid())

    

#login test
class Login(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="gustavo",
            password="123456"
        )
    def test_login_valid(self):
        self.assertEquals(self.user.username,'gustavo')
        self.assertEquals(self.user.password,'123456')


#por revisar
class TestBusForm(TestCase):
    def test_empty_form(self):
        #form_data = {'placa':'dc6-456','modelo':'yaris','marca':'toyota'}
        #form = BusForm(data=form_data)
        form = BusForm()
        self.assertTrue("modelo", form.fields)
        self.assertTrue("placa", form.fields)
        self.assertTrue("marca", form.fields)
