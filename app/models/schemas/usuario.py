"""Esquemas Pydantic para Usuario."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    password: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str]
    id_usuario_edicion: Optional[str]

    class Config:
        from_attributes = True