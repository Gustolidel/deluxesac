from django.shortcuts import render, redirect


from django.contrib.auth.models import User


from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CargoForm,BusForm,EmpleadoForm,ActividadForm,AsistenciaForm, CreateUserForm
from .models import Cargo, Bus, Empleado, Actividad, Asistencia
from django.forms import inlineformset_factory
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.db.models import Sum, Count
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse, response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.urls import reverse_lazy
import csv
import xlwt

#PARA EXPORTAR PDF
import os

# insert the GTK3 Runtime folder at the beginning

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

# Create your views here.

@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Usuario o password son incorrectos')
    context = {}
    return render(request, 'administrador/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def indexPage(request):
    empleado = Empleado.objects.all()[:4]
    empleados = Empleado.objects.all()
    filtro_femenino_empleados = Empleado.objects.filter(genero=1)
    filtro_masculino_empleados = Empleado.objects.filter(genero=2)
    count_filtro_masculino_empleados = filtro_masculino_empleados.count()
    count_filtro_femenino_empleados = filtro_femenino_empleados.count()
    asistencias = Asistencia.objects.all()
    asistencias_count = asistencias.count()
    users = User.objects.all()
    today = datetime.today() + timedelta(days=1)
    last_week =  datetime.now() - timedelta(days=7)
    users_last_login = User.objects.filter(last_login__range=(last_week, today))
    users_empleados = users_last_login.filter(is_superuser=False)
    users_top = users_empleados[:2]
    empleados_count = empleados.count()
    users_count = users.count()
    filtro_asistencias = asistencias.filter(estado=1)
    filtro_asistencias_count = filtro_asistencias.count()
    porcentaje_asistencias = round((filtro_asistencias_count*(100/100)*100)/asistencias_count)
    filtro_inasistencias = asistencias.filter(estado=2)
    filtro_inasistencias_count = filtro_inasistencias.count()
    porcentaje_inasistencias = round((filtro_inasistencias_count*(100/100)*100)/asistencias_count)
    filtro_porrevisar = asistencias.filter(estado=3)
    filtro_porrevisar_count = filtro_porrevisar.count()
    porcentaje_porrevisar = round((filtro_porrevisar_count*(100/100)*100)/asistencias_count)
    last_month = datetime.today() - timedelta(days=30)
    filtro_asistencias_estado1 = filtro_asistencias.filter(fecha__gte=last_month)
    filtro_asistencias_estado2 = filtro_inasistencias.filter(fecha__gte=last_month)
    filtro_asistencias_estado3 = filtro_porrevisar.filter(fecha__gte=last_month)
    filtro_asistencias_estado1_count = filtro_asistencias_estado1.count()
    filtro_asistencias_estado2_count = filtro_asistencias_estado2.count()
    filtro_asistencias_estado3_count = filtro_asistencias_estado3.count()
    context = {'count_filtro_femenino_empleados':count_filtro_femenino_empleados,'count_filtro_masculino_empleados':count_filtro_masculino_empleados,'users_top':users_top,'porcentaje_porrevisar':porcentaje_porrevisar,'asistencias_count': asistencias_count,'asistencias':asistencias,'porcentaje_inasistencias':porcentaje_inasistencias,'porcentaje_asistencias':porcentaje_asistencias,'filtro_asistencias_estado2_count':filtro_asistencias_estado2_count,'filtro_asistencias_estado3_count':filtro_asistencias_estado3_count,'filtro_asistencias_estado1_count':filtro_asistencias_estado1_count,'filtro_porrevisar':filtro_porrevisar,'filtro_inasistencias':filtro_inasistencias,'filtro_asistencias':filtro_asistencias,'empleados':empleado, 'empleados_count':empleados_count, 'users_count':users_count}
    return render(request, 'administrador/index.html', context)


@login_required(login_url='login')
def errorPage(request):
    context = {}
    return render(request, 'administrador/error.html', context)


@login_required(login_url='login')
@admin_only
def reportesPage(request):
    if request.method=="POST":
        fechainicio = request.POST.get('fechainicio')
        fechafinal = request.POST.get('fechafinal')
        resultadobusqueda = Asistencia.objects.raw('select id, Empleado_id, Cargo_id, fecha, horaentrada, horasalida, estado from deluxeapp_asistencia where fecha between "'+ fechainicio +'" and "'+ fechafinal +'"')
        return render(request,'administrador/reportes.html',{'reportes':resultadobusqueda,'fechafinal':fechafinal,'fechainicio':fechainicio})
    else:
        reportes = Asistencia.objects.all()
        context = {'reportes':reportes }
        return render(request,'administrador/reportes.html', context)


@login_required(login_url='login')
@admin_only
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename=Reporte' + \
        str(datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['ID','Empleado','Cargo','Fecha','Hora Entrada', 'Hora Salida','Estado'])
    reportes = Asistencia.objects.all()
    for reporte in reportes:
        writer.writerow([reporte.id, reporte.Empleado, reporte.Cargo, 
        reporte.fecha, reporte.horaentrada, reporte.horasalida, reporte.estado])
    return response


@login_required(login_url='login')
@admin_only
def export_excel(request):
    response = HttpResponse(content_type="application/ms_excel")
    response['Content-Disposition'] = 'attachment; filename=Reporte' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reportes')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id','Empleado','Cargo','Fecha','Hora Entrada', 'Hora Salida','Estado']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = Asistencia.objects.all().values_list(
        'id', 'Empleado', 'Cargo', 'fecha', 'horaentrada', 'horasalida', 'estado')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)

    return response


def pdfpage(request):
    context = {}
    return render(request, 'administrador/pdf-output.html', context)

@login_required(login_url='login')
@admin_only
def export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline; attachment; filename=Reporte' + \
        str(datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    reportes = Asistencia.objects.all()
    total = reportes.count()

    html_string = render_to_string(
        'administrador/pdf-output.html', {'reportes':reportes, 'total': total}
    )
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required(login_url='login')
@admin_only
def tablesPage(request):
    cargo = Cargo.objects.all()
    empleado = Empleado.objects.all()
    context = {'cargos': cargo, 'empleados': empleado}
    return render(request, 'administrador/tables.html', context)


@login_required(login_url='login')
@admin_only
def asistenciasPage(request):
    asistencia = Asistencia.objects.all()
    context = {'asistencias': asistencia}
    return render(request, 'administrador/asistencias.html', context)


@login_required(login_url='login')
@admin_only
def createCargo(request):
    form = CargoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tables')
    return render(request, 'administrador/editCargo.html', {'form': form})


@login_required(login_url='login')
@admin_only
def updateCargo(request, id):
    cargos= Cargo.objects.get(id=id)
    form=CargoForm(request.POST or None, instance=cargos)
    if form.is_valid():
        form.save()
        return redirect('tables')
    return render(request, 'administrador/editCargo.html',{'form':form,'cargo': cargos})


@login_required(login_url='login')
@admin_only
def deleteCargo(request, id):
    cargo = Cargo.objects.get(id=id)
    if request.method == 'POST':
        cargo.delete()
        return redirect('tables')
    return render(request, 'administrador/deleteCargo.html', {'cargo': cargo})


@login_required(login_url='login')
@admin_only
def createEmpleado(request):
    form=EmpleadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tables')
    return render(request, 'administrador/editEmpleado.html', {'form':form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado','admin'])
def updateEmpleado(request, id):
    empleados=Empleado.objects.get(id=id)
    form=EmpleadoForm(request.POST or None, instance=empleados)
    if form.is_valid():
        form.save()
        return redirect('tables')
    return render(request, 'administrador/editEmpleado.html',{'form': form, 'empleado':empleados})


@login_required(login_url='login')
@admin_only
def deleteEmpleado(request,id):
    empleado=Empleado.objects.get(id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('tables')
    return render(request, 'administrador/deleteEmpleado.html', {'empleado':empleado})


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class createBus(View):
    def get(self, request):
        placa1 = request.GET.get('placa', None)
        modelo1 = request.GET.get('modelo', None)
        marca1 = request.GET.get('marca', None)

        obj = Bus.objects.create(
            placa = placa1,
            modelo = modelo1,
            marca = marca1
        )

        bus = {'id': obj.id, 'placa': obj.placa, 'modelo':obj.modelo, 'marca':obj.marca}

        data = {
            'bus': bus
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class CrudBus(ListView):
    model = Bus
    placas = Bus.objects.filter()
    template_name = 'administrador/buses.html'
    context_object_name = 'buses'


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class UpdateCrudBus(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        placa1 = request.GET.get('placa', None)
        modelo1 = request.GET.get('modelo', None)
        marca1 = request.GET.get('marca', None)

        obj = Bus.objects.get(id=id1)
        obj.placa = placa1
        obj.modelo = modelo1
        obj.marca = marca1
        obj.save()

        bus = {'id':obj.id, 'placa':obj.placa, 'modelo': obj.modelo, 'marca': obj.marca}

        data = {
            'bus':bus
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class DeleteCrudBus(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Bus.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


@login_required(login_url='login')
@admin_only
def userPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='empleado')
            user.groups.add(group)
            Empleado.objects.create(
                user=user,
                nombre=username
            )
            messages.success(request, "Cuenta registrada correctamente para "+username)
            return redirect('user')

    context = {'form': form}
    return render(request, 'administrador/user.html', context)


@login_required(login_url='login')
@admin_only
def createAsistencia(request):
    form = AsistenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('revisar')
    return render(request, 'administrador/editAsistencias.html', {'form':form})


@login_required(login_url='login')
@admin_only
def updateAsistencia(request, id):
    asistencias = Asistencia.objects.get(id=id)
    form = AsistenciaForm(request.POST or None, instance=asistencias)
    if form.is_valid():
        form.save()
        return redirect('revisar')
    return render(request, 'administrador/editAsistenciasAdmin.html', {'form': form,'asistencia': asistencias})


@login_required(login_url='login')
@admin_only
def deleteAsistencia(request, id):
    asistencia = Asistencia.objects.get(id=id)
    if request.method == 'POST':
        asistencia.delete()
        return redirect('revisar')
    return render(request, 'administrador/editAsistenciasAdmin.html', {'asistencia': asistencia})


@login_required(login_url='login')
@admin_only
def revisarPage(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'administrador/arevisar.html', {'asistencias':asistencia})


@login_required(login_url='login')
@admin_only
def inasistenciasPage(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'administrador/inasistencias.html', {'asistencias':asistencia})


@login_required(login_url='login')
@admin_only
def updateInasistencia(request, id):
    asistencias = Asistencia.objects.get(id=id)
    form = AsistenciaForm(request.POST or None, instance=asistencias)
    if form.is_valid():
        form.save()
        return redirect('inasistencias')
    return render(request, 'administrador/editAsistenciasAdmin.html', {'form': form,'asistencia': asistencias})


@login_required(login_url='login')
@admin_only
def deleteInasistencia(request, id):
    asistencia = Asistencia.objects.get(id=id)
    if request.method == 'POST':
        asistencia.delete()
        return redirect('inasistencias')
    return render(request, 'administrador/editAsistenciasAdmin.html', {'asistencia': asistencia})


@login_required(login_url='login')
@admin_only
def updateRevisar(request, id):
    asistencias = Asistencia.objects.get(id=id)
    form = AsistenciaForm(request.POST or None, instance=asistencias)
    if form.is_valid():
        form.save()
        return redirect('revisar')
    return render(request, 'administrador/editAsistenciasAdmin.html', {'form': form,'asistencia': asistencias})


@login_required(login_url='login')
@admin_only
def deleteRevisar(request, id):
    asistencia = Asistencia.objects.get(id=id)
    if request.method == 'POST':
        asistencia.delete()
        return redirect('revisar')
    return render(request, 'administrador/editAsistenciasAdmin.html', {'asistencia': asistencia})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado'])
def indexUserPage(request):
    empleado = Empleado.objects.all()
    return render(request, 'administrador/indexUser.html', {'empleados': empleado})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado'])
def misAsistenciasPage(request):
    asistencia = Asistencia.objects.all()
    misAsistencias = request.user.empleado.asistencia_set.all()
    filtro_misAsistencias = misAsistencias.filter(estado=1)
    return render(request, 'administrador/misAsistencias.html', {'filtro_misAsistencias':filtro_misAsistencias,'asistencias':asistencia, 'misAsistencias':misAsistencias})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado'])
def misInasistenciasPage(request):
    asistencia = Asistencia.objects.all()
    misInasistencias = request.user.empleado.asistencia_set.all()
    filtro_misInasistencias = misInasistencias.filter(estado=2)
    return render(request, 'administrador/misInasistencias.html', {'filtro_misInasistencias':filtro_misInasistencias,'asistencias':asistencia, 'misInasistencias':misInasistencias})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado'])
def misEnviadasPage(request):
    asistencia = Asistencia.objects.all()
    misEnviadas = request.user.empleado.asistencia_set.all()
    filtro_misEnviadas = misEnviadas.filter(estado=3)
    return render(request, 'administrador/misEnviadas.html', {'filtro_misEnviadas':filtro_misEnviadas,'asistencias':asistencia, 'misEnviadas':misEnviadas})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado'])
def createMiasistencia(request):
    form = AsistenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('misEnviadas')
    return render(request, 'administrador/editAsistencias.html',{'form':form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['empleado'])
def deleteMiasistencia(request, id):
    asistencia = Asistencia.objects.get(id=id)
    if request.method == 'POST':
        asistencia.delete()
        return redirect('misEnviadas')
    return render(request, 'administrador/deleteMisAsistencias.html',{'asistencia':asistencia})


@login_required(login_url='login')
@admin_only
def updateAdmin(request, id):
    admin = User.objects.get(id=id)
    form = CreateUserForm(request.POST or None, instance=admin)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'administrador/editAdmin.html', {'form': form,'admin': admin})