from django.urls import path
from . import views

urlpatterns = [
    path('', views.listaCliente.as_view()),
    path('cedula', views.cedulaCliente.as_view()),
    path('apellido', views.apellidoCliente.as_view()),
]