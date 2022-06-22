"""DeLuxe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from deluxeapp import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginPage, name='login'),
    path('index/', views.indexPage, name='index'),
    path('tables/', views.tablesPage, name='tables'),
    path('newCargo/', views.createCargo, name='createCargo'),
    path('deleteCargo/<int:id>/', views.deleteCargo, name='deleteCargo'),
    path('updateCargo/<int:id>/', views.updateCargo, name="updateCargo"),
    path('newEmpleado/', views.createEmpleado, name="createEmpleado"),
    path('deleteEmpleado/<int:id>/', views.deleteEmpleado, name='deleteEmpleado'),
    path('updateEmpleado/<int:id>/', views.updateEmpleado, name="updateEmpleado"),
    path('Buses/', views.CrudBus.as_view(), name="Buses"),
    path('newBus/', views.createBus.as_view(), name="createBus"),
    path('updateBus/', views.UpdateCrudBus.as_view(), name="updateBus"),
    path('deleteBus/', views.DeleteCrudBus.as_view(), name="deleteBus"),
    path('asistencias/', views.asistenciasPage, name='asistencias'),
    path('newAsistencia/', views.createAsistencia, name='createAsistencia'),
    path('updateAsistencia/<int:id>/', views.updateAsistencia, name='updateAsistencia'),
    path('deleteAsistencia/<int:id>/', views.deleteAsistencia, name='deleteAsistencia'),
    path('revisar/', views.revisarPage, name='revisar'),
    path('updateRevisar/<int:id>/', views.updateRevisar, name='updateRevisar'),
    path('deleteRevisar/<int:id>/', views.deleteRevisar, name='deleteRevisar'), 
    path('inasistencias/', views.inasistenciasPage, name='inasistencias'),
    path('updateInasistencia/<int:id>/', views.updateInasistencia, name='updateInasistencia'),
    path('deleteInasistencia/<int:id>/', views.deleteInasistencia, name='deleteInasistencia'),
    path('user/', views.userPage, name='user'),
    path('logout/', views.logoutUser, name='logout'),
    path('error/', views.errorPage, name='error'),
    path('indexUser/', views.indexUserPage, name="indexUser"),
    path('misAsistencias/', views.misAsistenciasPage, name='misAsistencias'),
    path('misInasistencias/', views.misInasistenciasPage, name='misInasistencias'),
    path('misEnviadas/', views.misEnviadasPage, name='misEnviadas'),
    path('newMiasistencia/', views.createMiasistencia, name="createMiasistencia"),
    path('deleteMiasistencia/<int:id>/', views.deleteMiasistencia, name='deleteMiasistencia'),
    path('reportes/', views.reportesPage, name='reportes'),
    path('export_csv',views.export_csv, name='export_csv'),
    path('export_excel',views.export_excel, name='export_excel'),
    path('export_pdf',views.export_pdf, name='export_pdf'),
    path('pdfpage', views.pdfpage, name='pdfpage'),
    path('updateAdmin/<int:id>/', views.updateAdmin, name='updateAdmin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
