"""Esquemas Pydantic para Mantenimiento."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class MantenimientoBase(BaseModel):
    vehiculo_id: str
    contrato_id: Optional[str] = None
    tipo: str = "Limpieza"
    descripcion: Optional[str] = None
    costo: Decimal = 0.0
    fecha_solicitud: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None
    estado: str = "Pendiente"

class MantenimientoCreate(MantenimientoBase):
    pass

class MantenimientoResponse(MantenimientoBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str]
    id_usuario_edicion: Optional[str]

    class Config:
        from_attributes = True