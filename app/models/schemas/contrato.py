"""Esquemas Pydantic para Contrato."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ContratoBase(BaseModel):
    cliente_id: str
    vehiculo_id: str
    horas_contratadas: int
    precio_por_hora: Decimal
    precio_total: Decimal
    pagado: bool = False
    fecha_inicio: Optional[datetime] = None
    fecha_fin_estimada: datetime
    fecha_fin_real: Optional[datetime] = None

class ContratoCreate(ContratoBase):
    pass

class ContratoResponse(ContratoBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str]
    id_usuario_edicion: Optional[str]

    class Config:
        from_attributes = True