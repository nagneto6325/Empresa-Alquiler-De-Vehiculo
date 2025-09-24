"""Modelo de Pago para la base de datos."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from database import Base

class Pago(Base):
    """Modelo de pago con control de auditoria."""

    __tablename__ = "pagos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contrato_id = Column(String(36), ForeignKey("contratos.id"), nullable=False)
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(String(50), default="Efectivo")
    fecha_pago = Column(DateTime, nullable=False)
    estado = Column(String(20), default="Completado")

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    id_usuario_creacion = Column(String(36), nullable=True)
    id_usuario_edicion = Column(String(36), nullable=True)

    def __str__(self):
        return f"Pago {self.id} - ${self.monto}"