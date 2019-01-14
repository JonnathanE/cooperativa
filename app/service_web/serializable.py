from rest_framework import serializers
from app.modelo.models import Cliente

class ClienteSerializable(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos", "genero", "estadoCivil", "fechaNacimiento", "correo", "telefono", "celular", "direccion"]