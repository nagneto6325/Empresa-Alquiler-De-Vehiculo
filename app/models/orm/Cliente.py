"""Modelo de Cliente para la base de datos."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from database import Base

class Cliente(Base):
    """Modelo de cliente con control de auditoria."""

    __tablename__ = "clientes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100), nullable=True)
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    id_usuario_creacion = Column(String(36), nullable=True)
    id_usuario_edicion = Column(String(36), nullable=True)

    def __str__(self):
        return f"{self.nombre} (Usuario: {self.usuario_id})"