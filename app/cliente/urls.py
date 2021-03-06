from django.urls import path

from . import views

urlpatterns = [
    path('', views.principal, name = 'cliente'),
    path('prinBusc', views.principalBuscador, name='principalBuscador'),
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
    path('desactivarCuenta', views.desactivarEstadoCuenta),
    path('buscarCuenta', views.buscarCuenta),
    #url transaccion
    path('crearTransaccionNumeroCuenta', views.crearTransaccionNumeroCuenta),
    path('crearTransaccion', views.crearTransaccion),
    path('listarTransaccion', views.listarTransaccion),
    path('detalleCliente',views.detalleCilente, name = 'pruebaModal'),
    path('crearTransferenciaNumCuenta', views.crearTransferenciaNumeroCuenta),
    path('crearTransferencia', views.crearTransferencia),
    #crear pdf
    path('report', views.reporte_pdf),
    path('comprovante', views.transferencia_pdf),
    #otro
    path('buscarAjax', views.buscarCuentaAjax, name="buscarTransferenciaOrigen"),
    path('crearTransaccionAjax', views.crearTransaccionAjax),
]
