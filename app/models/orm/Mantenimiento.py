"""Modelo de Mantenimiento para la base de datos."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Text, ForeignKey
from database import Base

class Mantenimiento(Base):
    """Modelo de mantenimiento con control de auditoria."""

    __tablename__ = "mantenimientos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehiculo_id = Column(String(36), ForeignKey("vehiculos.id"), nullable=False)
    contrato_id = Column(String(36), ForeignKey("contratos.id"), nullable=True)
    tipo = Column(String(50), default="Limpieza")
    descripcion = Column(Text, nullable=True)
    costo = Column(Numeric(10, 2), default=0.0)
    fecha_solicitud = Column(DateTime, nullable=False)
    fecha_completado = Column(DateTime, nullable=True)
    estado = Column(String(20), default="Pendiente")

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    id_usuario_creacion = Column(String(36), nullable=True)
    id_usuario_edicion = Column(String(36), nullable=True)

    def __str__(self):
        return f"Mantenimiento {self.id} - {self.tipo}"