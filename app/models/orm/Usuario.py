"""Modelo de Usuario para la base de datos."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from database import Base

class Usuario(Base):
    """Modelo de usuario con control de auditoria."""

    __tablename__ = "usuarios"  # ✅ NOMBRE CORRECTO

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    id_usuario_creacion = Column(String(36), nullable=True)
    id_usuario_edicion = Column(String(36), nullable=True)

    def __str__(self):
        return f"{self.username} ({self.id})"