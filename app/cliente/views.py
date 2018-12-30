from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FormularioCliente, FormularioCuenta, FormularioTransaccion, FormularioCuentaCedula, FormularioBancaVirtual, FormularioTansferencia
from app.modelo.models import Cliente, Cuenta, Transaccion, Caja, BancaVirtual
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def principal(request):
    usuario = request.user
    #print(usuario.get_all_permissions())
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
        #messages.warning(request, 'No Permitido')
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
        auxC = Cliente.objects.filter(cedula=dni)
        if auxC:
            listaClientes = auxC.get(cedula=dni)
            if listaClientes:
                context = {
                    'item': listaClientes,
                    'title': "Clientes",
                    'mensaje': "Modulo Clientes"
                }
                return render(request, 'cliente/buscar_cliente.html', context)
            else:
                return redirect(principal)
        else:
            return redirect(principal)

    else:
        return render(request, 'login/acceso_prohibido.html')

def detalleCilente(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cliente'):
        dni = request.GET['cedula']
        cliente = Cliente.objects.get(cedula=dni)
        #formulario = FormularioCliente(instance=cliente)
        context = {
            'cliente': cliente,
            'title': "Modificar Cliente",
            'mensaje': "Modificar datos de " + cliente.nombres + " " + cliente.apellidos
        }
        return render(request, 'cliente/detalle_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')


#METODOS DE LA CUENTA
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


@login_required
def crearCuentaCedula(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cuenta'):
        formulario = FormularioCuentaCedula(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                dni = request.GET['cedula']
                cliente = Cliente.objects.get(cedula = dni)
                cuenta = Cuenta()
                cuenta.numero = datos.get('numero')
                cuenta.estado = True
                cuenta.saldo = datos.get('saldo')
                cuenta.tipoCuenta = datos.get('tipoCuenta')
                cuenta.cliente = cliente
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

@login_required
def listarCuenta (request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        dni = request.GET['cedula']
        client = Cliente.objects.get(cedula = dni)
        listaCuenta = Cuenta.objects.all().filter(cliente = client).order_by('numero')
        context = {
            'cuentas':listaCuenta,
            'mensaje':"Cuenta de "+client.nombres,
        }
        return render(request, 'cuenta/home_cuenta.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

@login_required
def principalCuenta(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        listaCuenta = Cuenta.objects.all().order_by('numero')
        context = {
            'cuentas': listaCuenta,
            'title': "Clientes",
            'mensaje': "Modulo Cuentas"
        }
        return render(request, 'cuenta/home_cuenta.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

@login_required
def activarEstadoCuenta(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cuenta'):
        num = request.GET['numero']
        if request.method == 'POST':
            cuenta = Cuenta.objects.get(numero = num)
            cuenta.estado = True
            cuenta.save()
            return redirect(principal)
        else:
            return render(request, 'cuenta/activar_cuenta.html')
    else:
        return render(request, 'login/acceso_prohibido.html')

@login_required
def buscarCuenta(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        num = request.GET['numero']
        auxC = Cuenta.objects.filter(numero=num)
        if auxC:
            listaCuenta = auxC.get(numero=num)
            if listaCuenta:
                context = {
                    'item': listaCuenta,
                    'title': "Clientes",
                    'mensaje': "Modulo Cuentas"
                }
                return render(request, 'cuenta/buscar_cuenta.html', context)
            else:
                return redirect(principal)
        else:
            return redirect(principal)

    else:
        return render(request, 'login/acceso_prohibido.html')

# METODOS DE TRANSACCION
@login_required
def listarTransaccion(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_transaccion'):
        num = request.GET['numero']
        cuent = Cuenta.objects.get(numero = num)
        listaTransaccion = Transaccion.objects.all().filter(cuenta = cuent).order_by('fecha')
        context = {
            'transacciones':listaTransaccion,
            'mensaje':"Transacciones de " + cuent.cliente.nombres,
        }
        return render(request, 'transaccion/home_transaccion.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

@login_required
def crearTransaccion (request):
    usuario = request.user
    if usuario.has_perm('modelo.add_transaccion'):
        formulario = FormularioTransaccion(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                #dni = request.GET['cedula']
                #cliente = Cliente.objects.get(cedula = dni)
                cuenta = datos.get('cuenta')
                if datos.get('tipo') == "retiro" or datos.get('tipo') == "online":
                    if saldo(cuenta.saldo,datos.get('valor')):
                        transaccion = Transaccion()
                        guardar_transaccion(transaccion, datos)
                        caja = Caja()
                        guardar_caja(caja, transaccion, usuario)
                        cuenta.saldo = cuenta.saldo-transaccion.valor
                        cuenta.save()
                        return redirect(principal)
                    else:
                        html = "<html><body>No se puede realizar el retiro.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                        return HttpResponse(html)
                elif datos.get('tipo') == "deposito" or datos.get('tipo') == "pensiones" or datos.get('tipo') == "seguros" or datos.get('tipo') == "iess":
                    transaccion = Transaccion()
                    guardar_transaccion(transaccion, datos)
                    caja = Caja()
                    guardar_caja(caja, transaccion, usuario)
                    cuenta.saldo = cuenta.saldo+transaccion.valor
                    cuenta.save()
                    return redirect(principal)
                elif datos.get('tipo') == "transferencia":
                    html = "<html><body>No se puede realizar la transferencia.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                    return HttpResponse(html)
        context = {
            'f': formulario,
            'title': "Ingresar Cuenta",
            'mensaje': "Ingresar nueva Transaccion",
        }
        return render(request, 'transaccion/crear_transaccion.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

def saldo(saldo, valor):
    if saldo >= valor:
        return True
    else:
        return False

def guardar_transaccion(transaccion, datos):
    transaccion.tipo = datos.get('tipo')
    transaccion.valor = datos.get('valor')
    transaccion.descripcion = datos.get('descripcion')
    transaccion.cuenta = datos.get('cuenta')
    transaccion.save()

def guardar_caja(caja, transaccion, usuario):
    caja.nombres = usuario.first_name
    caja.apellidos = usuario.last_name
    caja.transaccion = transaccion
    caja.save()


@login_required
def crearTransferencia(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_transaccion'):
        formulario = FormularioTansferencia(request.POST)
        form = FormularioBancaVirtual(request.POST)
        if request.method == 'POST':
            if formulario.is_valid() and form.is_valid():
                datosA = formulario.cleaned_data
                datosB = form.cleaned_data
                aux = Cuenta.objects.filter(numero = datosB.get('numeroCuentaDestino'))
                if aux:
                    cuentaB = aux.get(numero = datosB.get('numeroCuentaDestino'))
                    if cuentaB:
                        cuenta = datosA.get('cuenta')
                        if saldo(cuenta.saldo, datosA.get('valor')):
                            #guradar transaccion
                            transaccion = Transaccion()
                            transaccion.tipo = 'transferencia'
                            transaccion.valor = datosA.get('valor')
                            transaccion.descripcion = datosA.get('descripcion')
                            transaccion.cuenta = datosA.get('cuenta')
                            transaccion.save()
                            #guardar bancaVirtual
                            banca = BancaVirtual()
                            banca.numeroCuentaDestino = datosB.get('numeroCuentaDestino')
                            banca.dniTitularCuentaDestino = datosB.get('dniTitularCuentaDestino')
                            banca.titularCuentaDestino = datosB.get('titularCuentaDestino')
                            banca.transaccion = transaccion
                            banca.save()
                            #realizamos la transferencia
                            cuenta.saldo = cuenta.saldo - transaccion.valor
                            cuentaB.saldo = cuentaB.saldo + transaccion.valor
                            cuenta.save()
                            cuentaB.save()
                            return redirect(principal)
                        else:
                            html = "<html><body>No se puede realizar la transaccion.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                            return HttpResponse(html)
                    else:
                        html = "<html><body>No existe el numero de cuenta.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                        return HttpResponse(html)
                else:
                    html = "<html><body>No existe el numero de cuenta.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                    return HttpResponse(html)
        context = {
            'f': formulario,
            'b': form,
            'title': "Ingresar Cuenta",
            'mensaje': "Ingresar nueva Transferencia"
        }
        return render(request, 'transaccion/crear_transferencia.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')
