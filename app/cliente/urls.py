from django.urls import path

from . import views

urlpatterns = [
    path('', views.principal, name = 'cliente'),
    path('primerMensaje', views.saludar),
    path('nuevo', views.crear),
    path('editar', views.modificar),
    path('eliminar', views.eliminar),
    path('buscarCliente', views.buscarCliente),
    path('detalleCliente',views.detalleCilente, name = 'pruebaModal'),
    #url de cuenta
    path('crearCuenta', views.crearCuenta),
    path('crearCuentaCedula', views.crearCuentaCedula),
    path('listarCuenta', views.listarCuenta),
    path('listarAllCuentas', views.principalCuenta, name='listAllCuenta'),
    path('activarCuenta', views.activarEstadoCuenta),
    path('buscarCuenta', views.buscarCuenta),
    #url transaccion
    path('crearTransaccion', views.crearTransaccion),
    path('listarTransaccion', views.listarTransaccion),
    path('detalleCliente',views.detalleCilente, name = 'pruebaModal'),
    path('crearTransferencia', views.crearTransferencia),
]
