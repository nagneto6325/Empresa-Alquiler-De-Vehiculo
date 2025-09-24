"""Paquete principal de modelos."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .models.orm.Usuario import Usuario
from .models.orm.Cliente import Cliente
from .models.orm.Vehiculo import Vehiculo
from .models.orm.Contrato import Contrato
from .models.orm.Pago import Pago
from .models.orm.Mantenimiento import Mantenimiento

__all__ = [
    "Base",
    "Usuario",
    "Cliente",
    "Vehiculo",
    "Contrato",
    "Pago",
    "Mantenimiento"
]