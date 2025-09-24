"""Modelo de Contrato para la base de datos."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Numeric, ForeignKey
from database import Base

class Contrato(Base):
    """Modelo de contrato con control de auditoria."""

    __tablename__ = "contratos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False)
    vehiculo_id = Column(String(36), ForeignKey("vehiculos.id"), nullable=False)
    horas_contratadas = Column(Integer, nullable=False)
    precio_por_hora = Column(Numeric(10, 2), nullable=False)
    precio_total = Column(Numeric(10, 2), nullable=False)
    pagado = Column(Boolean, default=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin_estimada = Column(DateTime, nullable=False)
    fecha_fin_real = Column(DateTime, nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    id_usuario_creacion = Column(String(36), nullable=True)
    id_usuario_edicion = Column(String(36), nullable=True)

    def __str__(self):
        return f"Contrato {self.id} - ${self.precio_total}"