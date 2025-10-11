"""Esquemas Pydantic para Pago."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class PagoBase(BaseModel):
    contrato_id: str
    cliente_id: str
    monto: Decimal
    metodo_pago: str = "Efectivo"
    fecha_pago: Optional[datetime] = None
    estado: str = "Completado"

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str]
    id_usuario_edicion: Optional[str]

    class Config:
        from_attributes = True