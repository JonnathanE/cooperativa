from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FormularioCliente, FormularioCuenta
from app.modelo.models import Cliente, Cuenta
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def principal(request):
    usuario = request.user
    print(usuario.get_all_permissions())
    if usuario.has_perm('modelo.view_cliente'):
        listaClientes = Cliente.objects.all().order_by('apellidos')
        context = {
            'clientes': listaClientes,
            'title': "Clientes",
            'mensaje': "Modulo Clientes"
        }
        return render(request, 'cliente/home_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')

def saludar(request):
    return HttpResponse('Hola clase')

@login_required
def crear(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cliente'):
        formulario = FormularioCliente(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cliente = Cliente()
                cliente.cedula = datos.get('cedula')
                cliente.nombres = datos.get('nombres')
                cliente.apellidos = datos.get('apellidos')
                cliente.genero = datos.get('genero')
                cliente.estadoCivil = datos.get('estadoCivil')
                cliente.fechaNacimiento = datos.get('fechaNacimiento')
                cliente.correo = datos.get('correo')
                cliente.telefono = datos.get('telefono')
                cliente.celular = datos.get('celular')
                cliente.direccion = datos.get('direccion')
                cliente.save()
                messages.warning(request, 'Guardado Exitosamente')
                return redirect(principal)
        context = {
            'f': formulario,
            'title': "Ingresar Cliente",
            'mensaje': "Ingresar Nuevo Cliente"
        }
        return render(request, 'cliente/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')

@login_required
def modificar(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cliente'):
        dni = request.GET['cedula']
        cliente = Cliente.objects.get(cedula=dni)
        formulario = FormularioCliente(instance=cliente)

        if request.method == 'POST':
            cliente.cedula = request.POST['cedula']
            cliente.apellidos = request.POST['apellidos']
            cliente.nombres = request.POST['nombres']
            cliente.genero = request.POST['genero']
            cliente.estadoCivil = request.POST['estadoCivil']
            cliente.fechaNacimiento = request.POST['fechaNacimiento']
            cliente.correo = request.POST['correo']
            cliente.telefono = request.POST['telefono']
            cliente.celular = request.POST['celular']
            cliente.direccion = request.POST['direccion']
            cliente.save()
            messages.warning(request, 'Datos Modificados')
            return redirect(principal)
        context = {
            'f': formulario,
            'title': "Modificar Cliente",
            'mensaje': "Modificar datos de " + cliente.nombres + " " + cliente.apellidos
        }
        return render(request, 'cliente/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')


@login_required
def eliminar(request):
    usuario = request.user
    if usuario.has_perm('modelo.delete_cliente'):
        dni = request.GET['cedula']
        cliente = Cliente.objects.get(cedula=dni)
        if cliente:
            if cliente.delete():
                messages.warning(request, 'Cliente Eliminado')
            else:
                messages.warning(request, 'No se pudo Eliminar')
            return redirect(principal)
        else:
            messages.warning(request, 'Perdido')
            return redirect(principal)
        return render(request, 'clientes/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')

@login_required
def buscarCliente(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cliente'):
        dni = request.GET['cedula']
        #cliente = Cliente.objects.get(cedula=dni)
        listaClientes = Cliente.objects.get(cedula=dni)
        context = {
            'item': listaClientes,
            'title': "Clientes",
            'mensaje': "Modulo Clientes"
        }
        return render(request, 'cliente/buscar_cliente.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

@login_required
def crearCuenta (request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cuenta'):
        formulario = FormularioCuenta(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                #dni = request.GET['cedula']
                #cliente = Cliente.objects.get(cedula = dni)
                cuenta = Cuenta()
                cuenta.numero = datos.get('numero')
                cuenta.estado = True
                cuenta.saldo = datos.get('saldo')
                cuenta.tipoCuenta = datos.get('tipoCuenta')
                cuenta.cliente = datos.get('cliente')
                #cuenta.cliente = cliente
                cuenta.save()
                return redirect(principal)
        context = {
            'f': formulario,
            'title': "Ingresar Cuenta",
            'mensaje': "Ingresar nueva Cuenta"
        }
        return render(request, 'cliente/crear_cliente.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

def listarCuenta (request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        dni = request.GET['cedula']
        client = Cliente.objects.get(cedula = dni)
        listaCuenta = Cuenta.objects.all().filter(cliente = client).order_by('numero')
        context = {
            'cuentas':listaCuenta,
            'mensaje':"Modulo Cuenta"
        }
        return render(request, 'cuenta/home_cuenta.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')