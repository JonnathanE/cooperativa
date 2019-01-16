from django import forms
from app.modelo.models import Cliente
from app.modelo.models import Cuenta
from app.modelo.models import Banco
from app.modelo.models import Transaccion
from app.modelo.models import BancaVirtual
from app.modelo.models import Caja
from app.modelo.models import CajeroAutomatico

# se crea un nuevo cliente
class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos", "genero", "estadoCivil", "fechaNacimiento", "correo", "telefono", "celular", "direccion"]

class FormularioBanco(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ["nombre", "direccion", "telefono", "correo"]

class FormularioCuenta(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ["numero", "estado", "saldo", "tipoCuenta", "cliente"]

# se crea una cuenta a traves de la cedula del cliente
class FormularioCuentaCedula(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ["numero", "saldo", "tipoCuenta"]

class FormularioTransaccion(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["tipo", "valor", "descripcion", "cuenta"]

#crear transaccion a traves del numero de cuenta
class FormularioTransaccionNumCuenta(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["tipo", "valor", "descripcion"]

#transferencia
class FormularioTansferencia(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["valor", "descripcion", "cuenta"]

# crear transferencia a traves del numero de cuenta
class FormularioTansferenciaNumCuenta(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["valor", "descripcion"]

        

# crear banca Virtual a traves del numero de cuenta
class FormularioBancaVirtualNumCuenta(forms.ModelForm):
    class Meta:
        model = BancaVirtual
        fields = ["numeroCuentaDestino"]


class FormularioBancaVirtual(forms.ModelForm):
    class Meta:
        model = BancaVirtual
        fields = ["numeroCuentaDestino", "dniTitularCuentaDestino", "titularCuentaDestino"]

class FormularioCaja(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ["nombres", "apellidos", "transaccion"]

class FormularioCajeroAutomatico(forms.ModelForm):
    class Meta:
        model = CajeroAutomatico
        fields = ["codigo", "ubicacion", "transaccion"]