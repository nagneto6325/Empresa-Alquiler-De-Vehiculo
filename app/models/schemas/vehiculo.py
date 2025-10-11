"""Esquemas Pydantic para Vehículo."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class VehiculoBase(BaseModel):
    nombre: str
    tipo: str
    tarifa_hora: Decimal
    disponible: bool = True
    necesita_mantenimiento: bool = False
    puertas: Optional[int] = None
    cilindraje: Optional[int] = None
    capacidad_carga: Optional[int] = None
    tipo_bici: Optional[str] = None
    autonomia_km: Optional[int] = None

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoResponse(VehiculoBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str]
    id_usuario_edicion: Optional[str]

    class Config:
        from_attributes = True