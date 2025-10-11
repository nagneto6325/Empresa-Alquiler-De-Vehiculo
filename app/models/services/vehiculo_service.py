"""Servicios para la gestión de vehículos."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.orm.Vehiculo import Vehiculo
from app.models.schemas.vehiculo import VehiculoCreate

class VehiculoService:
    """Servicio para operaciones de vehículos."""
    
    @staticmethod
    def crear_vehiculo(db: Session, vehiculo_data: VehiculoCreate) -> Vehiculo:
        """Crear un nuevo vehículo."""
        vehiculo = Vehiculo(
            **vehiculo_data.dict(),
            id_usuario_creacion="sistema"
        )
        
        db.add(vehiculo)
        db.commit()
        db.refresh(vehiculo)
        return vehiculo
    
    @staticmethod
    def obtener_vehiculo_por_id(db: Session, vehiculo_id: str) -> Optional[Vehiculo]:
        """Obtener vehículo por ID."""
        return db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    
    @staticmethod
    def listar_vehiculos(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        disponible: Optional[bool] = None,
        tipo: Optional[str] = None
    ) -> List[Vehiculo]:
        """Listar vehículos con filtros opcionales."""
        query = db.query(Vehiculo)
        
        if disponible is not None:
            query = query.filter(Vehiculo.disponible == disponible)
        
        if tipo:
            query = query.filter(Vehiculo.tipo == tipo)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def listar_vehiculos_disponibles(db: Session) -> List[Vehiculo]:
        """Listar vehículos disponibles para alquiler."""
        return db.query(Vehiculo).filter(
            Vehiculo.disponible == True,
            Vehiculo.necesita_mantenimiento == False
        ).all()
    
    @staticmethod
    def actualizar_vehiculo(
        db: Session, 
        vehiculo_id: str, 
        vehiculo_data: VehiculoCreate
    ) -> Vehiculo:
        """Actualizar vehículo existente."""
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehículo no encontrado"
            )
        
        for field, value in vehiculo_data.dict(exclude_unset=True).items():
            setattr(vehiculo, field, value)
        
        vehiculo.id_usuario_edicion = "sistema"
        db.commit()
        db.refresh(vehiculo)
        return vehiculo
    
    @staticmethod
    def eliminar_vehiculo(db: Session, vehiculo_id: str) -> bool:
        """Eliminar vehículo."""
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehículo no encontrado"
            )
        
        db.delete(vehiculo)
        db.commit()
        return True
    
    @staticmethod
    def marcar_como_mantenimiento(db: Session, vehiculo_id: str) -> Vehiculo:
        """Marcar vehículo como necesita mantenimiento."""
        vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehículo no encontrado"
            )
        
        vehiculo.necesita_mantenimiento = True
        vehiculo.disponible = False
        vehiculo.id_usuario_edicion = "sistema"
        
        db.commit()
        db.refresh(vehiculo)
        return vehiculo