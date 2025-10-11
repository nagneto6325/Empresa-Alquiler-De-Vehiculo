from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from database import SessionLocal
from app.models.orm.Mantenimiento import Mantenimiento as MantenimientoORM
from app.models.orm.Vehiculo import Vehiculo as VehiculoORM
from app.models.orm.Contrato import Contrato as ContratoORM

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MantenimientoBase(BaseModel):
    vehiculo_id: str
    contrato_id: Optional[str] = None
    tipo: str = "Limpieza"
    descripcion: Optional[str] = None
    costo: float = 0.0
    fecha_solicitud: datetime
    fecha_completado: Optional[datetime] = None
    estado: str = "Pendiente"
    id_usuario_creacion: Optional[str] = None

class MantenimientoCreate(MantenimientoBase):
    pass

class MantenimientoUpdate(MantenimientoBase):
    id_usuario_edicion: Optional[str] = None

class Mantenimiento(BaseModel):
    id: str
    vehiculo_id: str
    contrato_id: Optional[str] = None
    tipo: str
    descripcion: Optional[str] = None
    costo: float
    fecha_solicitud: datetime
    fecha_completado: Optional[datetime] = None
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str] = None
    id_usuario_edicion: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=Mantenimiento, status_code=status.HTTP_201_CREATED)
def crear_mantenimiento(mantenimiento: MantenimientoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo registro de mantenimiento en el sistema."""
    try:
        vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == mantenimiento.vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        if mantenimiento.contrato_id:
            contrato = db.query(ContratoORM).filter(ContratoORM.id == mantenimiento.contrato_id).first()
            if not contrato:
                raise HTTPException(status_code=404, detail="Contrato no encontrado")
        db_mantenimiento = MantenimientoORM(
            id=str(uuid.uuid4()),
            vehiculo_id=mantenimiento.vehiculo_id,
            contrato_id=mantenimiento.contrato_id,
            tipo=mantenimiento.tipo,
            descripcion=mantenimiento.descripcion,
            costo=mantenimiento.costo,
            fecha_solicitud=mantenimiento.fecha_solicitud,
            fecha_completado=mantenimiento.fecha_completado,
            estado=mantenimiento.estado,
            id_usuario_creacion=mantenimiento.id_usuario_creacion,
        )
        vehiculo.necesita_mantenimiento = True
        db.add(db_mantenimiento)
        db.commit()
        db.refresh(db_mantenimiento)
        return db_mantenimiento
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear mantenimiento: {str(e)}")

@router.get("/", response_model=List[Mantenimiento])
def listar_mantenimientos(db: Session = Depends(get_db)):
    """Obtener una lista con todos los mantenimientos registrados."""
    try:
        mantenimientos = db.query(MantenimientoORM).order_by(MantenimientoORM.fecha_creacion.desc()).all()
        return mantenimientos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar mantenimientos: {str(e)}")

@router.get("/{mantenimiento_id}", response_model=Mantenimiento)
def obtener_mantenimiento(mantenimiento_id: str, db: Session = Depends(get_db)):
    """Obtener un mantenimiento específico por su ID."""
    mantenimiento = db.query(MantenimientoORM).filter(MantenimientoORM.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento

@router.put("/{mantenimiento_id}", response_model=Mantenimiento)
def actualizar_mantenimiento(mantenimiento_id: str, mantenimiento: MantenimientoUpdate, db: Session = Depends(get_db)):
    """Actualizar la información de un mantenimiento existente."""
    try:
        db_mantenimiento = db.query(MantenimientoORM).filter(MantenimientoORM.id == mantenimiento_id).first()
        if not db_mantenimiento:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
        vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == mantenimiento.vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        if mantenimiento.contrato_id:
            contrato = db.query(ContratoORM).filter(ContratoORM.id == mantenimiento.contrato_id).first()
            if not contrato:
                raise HTTPException(status_code=404, detail="Contrato no encontrado")
        db_mantenimiento.vehiculo_id = mantenimiento.vehiculo_id
        db_mantenimiento.contrato_id = mantenimiento.contrato_id
        db_mantenimiento.tipo = mantenimiento.tipo
        db_mantenimiento.descripcion = mantenimiento.descripcion
        db_mantenimiento.costo = mantenimiento.costo
        db_mantenimiento.fecha_solicitud = mantenimiento.fecha_solicitud
        db_mantenimiento.fecha_completado = mantenimiento.fecha_completado
        db_mantenimiento.estado = mantenimiento.estado
        db_mantenimiento.id_usuario_edicion = mantenimiento.id_usuario_edicion
        if mantenimiento.estado == "Completado":
            vehiculo.necesita_mantenimiento = False
        else:
            vehiculo.necesita_mantenimiento = True
        db.commit()
        db.refresh(db_mantenimiento)
        return db_mantenimiento
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar mantenimiento: {str(e)}")

@router.delete("/{mantenimiento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mantenimiento(mantenimiento_id: str, db: Session = Depends(get_db)):
    """Eliminar un mantenimiento del sistema."""
    try:
        db_mantenimiento = db.query(MantenimientoORM).filter(MantenimientoORM.id == mantenimiento_id).first()
        if not db_mantenimiento:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
        vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == db_mantenimiento.vehiculo_id).first()
        if vehiculo:
            otros_mantenimientos = (
                db.query(MantenimientoORM)
                .filter(
                    MantenimientoORM.vehiculo_id == vehiculo.id,
                    MantenimientoORM.id != mantenimiento_id,
                    MantenimientoORM.estado != "Completado",
                )
                .count()
            )
            if otros_mantenimientos == 0:
                vehiculo.necesita_mantenimiento = False
        db.delete(db_mantenimiento)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar mantenimiento: {str(e)}")
