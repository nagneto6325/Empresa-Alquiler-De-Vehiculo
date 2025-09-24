"""Modelo de Vehiculo para la base de datos."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Numeric
from database import Base

class Vehiculo(Base):
    """Modelo de vehiculo con control de auditoria."""

    __tablename__ = "vehiculos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    tarifa_hora = Column(Numeric(10, 2), nullable=False)
    disponible = Column(Boolean, default=True)
    necesita_mantenimiento = Column(Boolean, default=False)

    puertas = Column(Integer, nullable=True)
    cilindraje = Column(Integer, nullable=True)
    capacidad_carga = Column(Integer, nullable=True)
    tipo_bici = Column(String(20), nullable=True)
    autonomia_km = Column(Integer, nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    id_usuario_creacion = Column(String(36), nullable=True)
    id_usuario_edicion = Column(String(36), nullable=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"