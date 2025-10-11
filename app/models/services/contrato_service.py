"""Servicios para la gestión de contratos."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.orm.Contrato import Contrato
from app.models.orm.Vehiculo import Vehiculo
from app.models.orm.Cliente import Cliente
from app.models.schemas.contrato import ContratoCreate

class ContratoService:
    """Servicio para operaciones de contratos."""
    
    @staticmethod
    def crear_contrato(db: Session, contrato_data: ContratoCreate) -> Contrato:
        """Crear un nuevo contrato de alquiler."""
        # Verificar que el vehículo existe y está disponible
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == contrato_data.vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehículo no encontrado"
            )
        
        if not vehiculo.disponible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El vehículo no está disponible"
            )
        
        # Verificar que el cliente existe
        cliente = db.query(Cliente).filter(Cliente.id == contrato_data.cliente_id).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Crear contrato
        contrato = Contrato(
            **contrato_data.dict(),
            id_usuario_creacion="sistema"
        )
        
        # Marcar vehículo como no disponible
        vehiculo.disponible = False
        vehiculo.id_usuario_edicion = "sistema"
        
        db.add(contrato)
        db.commit()
        db.refresh(contrato)
        return contrato
    
    @staticmethod
    def obtener_contrato_por_id(db: Session, contrato_id: str) -> Optional[Contrato]:
        """Obtener contrato por ID."""
        return db.query(Contrato).filter(Contrato.id == contrato_id).first()
    
    @staticmethod
    def listar_contratos_por_cliente(db: Session, cliente_id: str) -> List[Contrato]:
        """Listar contratos de un cliente específico."""
        return db.query(Contrato).filter(Contrato.cliente_id == cliente_id).all()
    
    @staticmethod
    def listar_contratos_activos(db: Session) -> List[Contrato]:
        """Listar contratos activos (sin fecha de fin real)."""
        return db.query(Contrato).filter(Contrato.fecha_fin_real == None).all()
    
    @staticmethod
    def finalizar_contrato(db: Session, contrato_id: str) -> Contrato:
        """Finalizar contrato estableciendo fecha de fin real."""
        contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
        if not contrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contrato no encontrado"
            )
        
        if contrato.fecha_fin_real:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El contrato ya está finalizado"
            )
        
        contrato.fecha_fin_real = datetime.utcnow()
        contrato.id_usuario_edicion = "sistema"
        
        # Liberar vehículo
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == contrato.vehiculo_id).first()
        if vehiculo:
            vehiculo.disponible = False  # No disponible hasta mantenimiento
            vehiculo.necesita_mantenimiento = True
            vehiculo.id_usuario_edicion = "sistema"
        
        db.commit()
        db.refresh(contrato)
        return contrato