from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FormularioCliente, FormularioCuenta, FormularioTransaccion, FormularioCuentaCedula, FormularioBancaVirtual, FormularioTansferencia
from app.modelo.models import Cliente, Cuenta, Transaccion, Caja, BancaVirtual
from django.contrib.auth.decorators import login_required

from io import BytesIO
from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4, cm
from django.http import FileResponse
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import pink, black, red, blue, green
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

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
        #messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')

def principalBuscador(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cliente'):
        return render(request, 'principal_busqueda.html')
    else:
        #messages.warning(request, 'No Permitido')
        return render(request, 'login/acceso_prohibido.html')

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
                messages.info(request, 'Guardado Exitosamente!!')
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
            messages.warning(request, 'Datos Modificados!!')
            return redirect(principal)
        context = {
            'f': formulario,
            'title': "Modificar Cliente",
            'mensaje': "Modificar datos de " + cliente.nombres + " " + cliente.apellidos,
            'dni': dni
        }
        return render(request, 'cliente/editar_cliente.html', context)
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
            messages.warning(request, 'Eliminado exitosamente!!')
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
                return redirect(principalBuscador)
        else:
            return redirect(principalBuscador)

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
                cuenta.saldoApertura = datos.get('saldo')
                cuenta.tipoCuenta = datos.get('tipoCuenta')
                cuenta.cliente = datos.get('cliente')
                #cuenta.cliente = cliente
                cuenta.save()
                messages.info(request, 'Cuenta creada exitosamente!!')
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
        dni = request.GET['cedula']
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                
                cliente = Cliente.objects.get(cedula = dni)
                cuenta = Cuenta()
                cuenta.numero = datos.get('numero')
                cuenta.estado = True
                cuenta.saldo = datos.get('saldo')
                cuenta.saldoApertura = datos.get('saldo')
                cuenta.tipoCuenta = datos.get('tipoCuenta')
                cuenta.cliente = cliente
                cuenta.save()
                messages.warning(request, 'Cuenta creada exitosamente!!')
                return redirect(principal)
        context = {
            'f': formulario,
            'title': "Ingresar Cuenta",
            'mensaje': "Ingresar nueva Cuenta",
            'dni': dni
        }
        return render(request, 'cuenta/crear_cuenta.html', context)
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
            return redirect(principalCuenta)
        else:
            context={
                'mensaje': "Desea Activar la Cuenta?",
                'enviar': "Activar",
            }
            return render(request, 'cuenta/activar_cuenta.html', context)
    else:
        return render(request, 'login/acceso_prohibido.html')

@login_required
def desactivarEstadoCuenta(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cuenta'):
        num = request.GET['numero']
        if request.method == 'POST':
            cuenta = Cuenta.objects.get(numero = num)
            cuenta.estado = False
            cuenta.save()
            return redirect(principalCuenta)
        else:
            context={
                'mensaje': "Desea Desactivar la Cuenta?",
                'enviar': "Desactivar",
            }
            return render(request, 'cuenta/activar_cuenta.html', context)
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
                return redirect(principalBuscador)
        else:
            return redirect(principalBuscador)

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
                if cuenta.estado == True:
                    if datos.get('tipo') == "retiro" or datos.get('tipo') == "online":
                        if saldo(cuenta.saldo,datos.get('valor')):
                            transaccion = Transaccion()
                            guardar_transaccion(transaccion, datos)
                            caja = Caja()
                            guardar_caja(caja, transaccion, usuario)
                            cuenta.saldo = cuenta.saldo-transaccion.valor
                            cuenta.save()
                            transaccion.saldoFinal = cuenta.saldo
                            transaccion.save()
                            messages.warning(request, 'Transaccion de RETIRO exitosa!!')
                            #return redirect(principal)
                            dat={
                                'cuentaA': cuenta,
                            }
                            return render(request, 'pdf/btn_cartola.html', dat)
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
                        transaccion.saldoFinal = cuenta.saldo
                        transaccion.save()
                        messages.warning(request, 'Transaccion de DEPOSITO exitoso!!')
                        #return redirect(principal)
                        dat={
                            'cuentaA': cuenta,
                        }
                        return render(request, 'pdf/btn_cartola.html', dat)
                    elif datos.get('tipo') == "transferencia":
                        html = "<html><body>No se puede realizar la transferencia.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                        return HttpResponse(html)
                else:
                    html = "<html><body>No se puede realizar la transferencia Debido a que su CUenta esta Inactiva.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
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
                            #guradar transaccion A
                            transaccion = Transaccion()
                            transaccion.tipo = 'transferencia'
                            transaccion.valor = datosA.get('valor')
                            transaccion.descripcion = datosA.get('descripcion')
                            transaccion.cuenta = datosA.get('cuenta')
                            transaccion.save()
                            #guradar transaccion B
                            transaccionB = Transaccion()
                            transaccionB.tipo = 'transferencia'
                            transaccionB.valor = datosA.get('valor')
                            transaccionB.descripcion = datosA.get('descripcion')
                            transaccionB.cuenta = cuentaB
                            transaccionB.save()
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
                            #se guarda el saldo final de la transaccion
                            transaccion.saldoFinal = cuenta.saldo
                            transaccion.save()
                            transaccionB.saldoFinal = cuentaB.saldo
                            transaccionB.save()
                            messages.warning(request, 'Transferencia exitosa!!')
                            #return redirect(principal)
                            dat={
                                'cuentaA': cuenta,
                                'cuentaB': cuentaB,
                                'transaccionA': transaccion,
                                'nombresA': cuenta.cliente.nombres,
                                'apellsA': cuenta.cliente.apellidos,
                                'direccionA': cuenta.cliente.direccion,
                                'telefonoA': cuenta.cliente.telefono,
                                'nombresBB': cuentaB.cliente.nombres,
                                'apellsBB': cuentaB.cliente.apellidos,
                            }
                            return render(request, 'pdf/btn.html', dat)
                        else:
                            html = "<html><body>No se puede realizar la transaccion debido a que no cuenta con el saldo suficiente.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                            return HttpResponse(html)
                    else:
                        html = "<html><body>No existe el numero de cuenta del destinatario.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                        return HttpResponse(html)
                else:
                    html = "<html><body>No existe el numero de cuenta.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
                    return HttpResponse(html)
            else:
                html = "<html><body>Los datos estan mal ingresados.<br><a href= "''">Volver</a> | <a href= "'listarAllCuentas'">Principal</a></body></html>"
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


# CREAR PDF

def reporte_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # Para descargar directo
    #response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
 
    # Create the PDF object, using the response object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer, A4)

    # Instanciar Cuenta
    num = request.GET['numero']
    cuent = Cuenta.objects.get(numero = num)
    #Instanciar Lista de transacciones
    listTransaccion = Transaccion.objects.all().filter(cuenta = cuent).order_by('fecha')

    # HEADER
    p.setLineWidth(.3)
    p.setFont('Helvetica', 10)
    p.drawString(180, 800, "COOPERATIVA DE AHORRO Y CREDITO")

    p.setFont('Helvetica-Bold', 17)
    p.drawString(160, 780, "COOPERATIVA JONNATHAN")

    p.setFont('Helvetica', 15)
    p.drawString(180, 762, "CUENTA TIPO: " + cuent.tipoCuenta)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(30, 730, "Oficina:")

    p.setFont('Helvetica', 12)
    p.drawString(95, 730, "Loja")

    p.setFont('Helvetica-Bold', 12)
    p.drawString(325, 730, "N. de Cuenta: ")
    p.setFont('Helvetica', 12)
    p.drawString(425, 730, cuent.numero)
    p.line(420, 727, 560, 727)#start X, height end y , height
    
    p.setFont('Helvetica-Bold', 12)
    p.drawString(30, 710, "Nombres:")

    p.setFont('Helvetica', 12)
    p.drawString(95, 710, cuent.cliente.apellidos + ' ' + cuent.cliente.nombres)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(30, 690, "Domicilio:")

    p.setFont('Helvetica', 12)
    p.drawString(95, 690, cuent.cliente.direccion)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(348, 690, "Telefono:")
    p.setFont('Helvetica', 12)
    p.drawString(425, 690, cuent.cliente.telefono)

    # Cliente table
    transacciones = []
    transacciones.append({'fecha':cuent.fechaApertura, 'name':"Apertura", 'b1':cuent.saldoApertura, 'b2':cuent.saldoApertura})
    for ltr in listTransaccion:
        transacciones.append({'fecha':ltr.fecha, 'name':ltr.tipo, 'b1':ltr.valor, 'b2':ltr.saldoFinal})
    #transacciones = [{'fecha':'1','name':'Jonnathan', 'b1':'3.4', 'b2':'3.5'}]

    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    fecha = Paragraph('''Fecha''', styleBH)
    tipo = Paragraph('''Tipo Operacion''', styleBH)
    monto = Paragraph('''Monto''', styleBH)
    saldo = Paragraph('''Saldo''', styleBH)

    data = []
    data.append([fecha, tipo, monto, saldo])

    # Table body
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    high = 640
    for t in transacciones:
        this_t = [t['fecha'], t['name'], t['b1'], t['b2']]
        data.append(this_t)
        high = high - 18
    
    # Table size
    table = Table(data, colWidths=[6 * cm, 6.4 * cm, 3 * cm, 3 * cm])
    table.setStyle(TableStyle([# estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    # pdf size
    width, height = A4
    table.wrapOn(p, width, height)
    table.drawOn(p, 30, high)
    # Close the PDF object cleanly, and we're done.
    p.showPage()# save page
    p.save() # save pdf
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def transferencia_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # Para descargar directo
    #response['Content-Disposition'] = 'attachment; filename=reporte.pdf'
 
    # Create the PDF object, using the response object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer, A4)

    # Instanciar Cuenta
    tipoCuenta = request.GET['tipocuenta']
    cuentaNumero = request.GET['cuentanumero']
    apellidos = request.GET['apellidosA']
    nombres = request.GET['nombresA']
    direccion = request.GET['direccion']
    telefono = request.GET['telefono']

    fechaTransaccion = request.GET['fecha']
    montoAux = request.GET['monto']
    numCuentaDestinatario = request.GET['numb']
    nombresDestinatario = request.GET['nomb']
    apellidosDestinatario = request.GET['apellb']
    
    # HEADER
    p.setLineWidth(.3)
    p.setFont('Helvetica', 10)
    p.drawString(180, 800, "COOPERATIVA DE AHORRO Y CREDITO")

    p.setFont('Helvetica-Bold', 17)
    p.drawString(160, 780, "COOPERATIVA JONNATHAN")

    p.setFont('Helvetica', 15)
    p.drawString(180, 762, "CUENTA TIPO: " + tipoCuenta)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(30, 730, "Oficina:")

    p.setFont('Helvetica', 12)
    p.drawString(95, 730, "Loja")

    p.setFont('Helvetica-Bold', 12)
    p.drawString(325, 730, "N. de Cuenta: ")
    p.setFont('Helvetica', 12)
    p.drawString(425, 730, cuentaNumero)
    p.line(420, 727, 560, 727)#start X, height end y , height
    
    p.setFont('Helvetica-Bold', 12)
    p.drawString(30, 710, "Nombres:")

    p.setFont('Helvetica', 12)
    p.drawString(95, 710, apellidos + ' ' + nombres)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(30, 690, "Domicilio:")

    p.setFont('Helvetica', 12)
    p.drawString(95, 690, direccion)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(348, 690, "Telefono:")
    p.setFont('Helvetica', 12)
    p.drawString(425, 690, telefono)

    
    # Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    fecha = Paragraph('''Fecha Emision''', styleBH)
    cuentaDestino = Paragraph('''Numero de Cuenta''', styleBH)
    destinatario = Paragraph('''Destinatario''', styleBH)
    tipo = Paragraph('''Tipo Operacion''', styleBH)
    monto = Paragraph('''Monto''', styleBH)

    data = []
    data.append([fecha, cuentaDestino, destinatario, tipo, monto])
    data.append([fechaTransaccion, numCuentaDestinatario, nombresDestinatario + apellidosDestinatario, "transferencia",montoAux])
    # Table body
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    high = 640
    
    # Table size
    table = Table(data, colWidths=[4.6 * cm, 2.5 * cm, 7 * cm, 3 * cm, 2.3 * cm])
    table.setStyle(TableStyle([# estilos de la tabla
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    # pdf size
    width, height = A4
    table.wrapOn(p, width, height)
    table.drawOn(p, 30, high)
    # Close the PDF object cleanly, and we're done.
    p.showPage()# save page
    p.save() # save pdf
    # get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
