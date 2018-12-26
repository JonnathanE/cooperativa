from django.urls import path

from . import views

urlpatterns = [
    path('', views.principal, name = 'cliente'),
    path('primerMensaje', views.saludar),
    path('nuevo', views.crear),
    path('editar', views.modificar),
    path('eliminar', views.eliminar),
    path('buscarCliente', views.buscarCliente),
    path('crearCuenta', views.crearCuenta),
    path('crearCuentaCedula', views.crearCuentaCedula),
    path('listarCuenta', views.listarCuenta),
    path('listarAllCuentas', views.principalCuenta, name='listAllCuenta'),
    path('activarCuenta', views.activarEstadoCuenta),
    path('crearTransaccion', views.crearTransaccion),
    path('listarTransaccion', views.listarTransaccion),
]
