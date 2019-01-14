from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from app.modelo.models import Cliente
from .serializable import ClienteSerializable
# Create your views here.

# Create your views here.
class listaCliente(APIView):
    def get(self, request):
        lista = Cliente.objects.all()#lista de objetos normales
        objetoSerializable = ClienteSerializable(lista, many = True)
        return Response(objetoSerializable.data)

class cedulaCliente(APIView):
    def get(self, request):
        dni = request.GET['cedula']
        lista = Cliente.objects.all().filter(cedula = dni)
        objetoSerializable = ClienteSerializable(lista, many = True)
        return Response(objetoSerializable.data)

class apellidoCliente(APIView):
    def get(self, request):
        apellido = request.GET['apellido']
        lista = Cliente.objects.all().filter(apellidos = apellido)
        objetoSerializable = ClienteSerializable(lista, many = True)
        return Response(objetoSerializable.data)
