"""Esquemas Pydantic para Cliente."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    contacto: Optional[str] = None
    usuario_id: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str]
    id_usuario_edicion: Optional[str]

    class Config:
        from_attributes = True