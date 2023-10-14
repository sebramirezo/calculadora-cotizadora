from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_login, name='redirect_login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('calculadora/', views.index, name='calculadora'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    ## Mantenedores y vistas de Recurso
    path('mantenedor_recursos', views.mantenedorRecurso, name='mantenedor_recursos'),
    path('edicionRecurso/<int:cod_rec>', views.edicionRecurso, name='edicionRecurso'),
    path('editarRecurso/', views.editarRecurso, name='editarRecurso'),
    ## Mantenedores y vistas de Servicio
    path('mantenedor_servicios', views.mantenedorServicio, name='mantenedor_servicios'),
    path('edicionServicio/<int:cod_servicio>', views.edicionServicio, name='edicionServicio'),
    path('editarServicio/', views.editarServicio, name='editarServicio'),
    path('registrarServicio/', views.registrarServicio, name='registrarServicio'),
    path('eliminarServicio/<cod_servicio>', views.eliminarServicio, name='eliminarServicio'),
    ## Mantenedores y vistas de Licencia
    path('mantenedor_licencias', views.mantenedorLicencias, name='mantenedor_licencias'),
    path('edicionLicencia/<int:cod_lic>', views.edicionLicencia, name='edicionLicencia'),
    path('editarLicencia/', views.editarLicencia, name='editarLicencia'),
    path('registrarLicencia/', views.registrarLicencia, name='registrarLicencia'),
    path('eliminarLicencia/<int:cod_lic>', views.eliminarLicencia, name='eliminarLicencia'),
    ## Mantenedores y vistas de Values
    path('mantenedor_values', views.mantenedorValues, name='mantenedor_values'),
    # Edición de los mantenedores por separado
    # Mantenedor ddValues
    path('edicionDdValue/<str:cod_value>', views.edicionDdValue, name='edicionDdValue'),
    path('editarDdValue/', views.editarDdValue, name='editarDdValue'),
    path('registrarDdValue/', views.registrarDdValue, name='registrarDdValue'),
    path('eliminarDdValue/<str:cod_value>', views.eliminarDdValue, name='eliminarDdValue'),
    ##
    # Mantenedor ramValues
    path('edicionRamValue/<str:cod_value>', views.edicionRamValue, name='edicionRamValue'),
    path('editarRamValue/', views.editarRamValue, name='editarRamValue'),
    path('registrarRamValue/', views.registrarRamValue, name='registrarRamValue'),
    path('eliminarRamValue/<str:cod_value>', views.eliminarRamValue, name='eliminarRamValue'),
    # Mantenedor cpuValues
    path('edicionCpuValue/<str:cod_value>', views.edicionCpuValue, name='edicionCpuValue'),
    path('editarCpuValue/', views.editarCpuValue, name='editarCpuValue'),
    path('registrarCpuValue/', views.registrarCpuValue, name='registrarCpuValue'),
    path('eliminarCpuValue/<str:cod_value>', views.eliminarCpuValue, name='eliminarCpuValue'),
]