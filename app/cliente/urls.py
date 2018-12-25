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
    path('listarCuenta', views.listarCuenta),
]