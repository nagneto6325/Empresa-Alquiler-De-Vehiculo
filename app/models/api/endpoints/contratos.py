from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from database import SessionLocal
from app.models.orm.Contrato import Contrato as ContratoORM
from app.models.orm.Cliente import Cliente as ClienteORM
from app.models.orm.Vehiculo import Vehiculo as VehiculoORM

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ContratoBase(BaseModel):
    cliente_id: str
    vehiculo_id: str
    horas_contratadas: int
    precio_por_hora: float
    pagado: bool = False
    fecha_inicio: datetime
    fecha_fin_estimada: datetime
    fecha_fin_real: Optional[datetime] = None
    id_usuario_creacion: Optional[str] = None

class ContratoCreate(ContratoBase):
    pass

class ContratoUpdate(ContratoBase):
    id_usuario_edicion: Optional[str] = None

class Contrato(BaseModel):
    id: str
    cliente_id: str
    vehiculo_id: str
    horas_contratadas: int
    precio_por_hora: float
    precio_total: float
    pagado: bool
    fecha_inicio: datetime
    fecha_fin_estimada: datetime
    fecha_fin_real: Optional[datetime] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str] = None
    id_usuario_edicion: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=Contrato, status_code=status.HTTP_201_CREATED)
def crear_contrato(contrato: ContratoCreate, db: Session = Depends(get_db)):
    try:
        cliente = db.query(ClienteORM).filter(ClienteORM.id == contrato.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == contrato.vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        if not vehiculo.disponible:
            raise HTTPException(status_code=400, detail="El vehículo no está disponible")

        precio_total = contrato.horas_contratadas * contrato.precio_por_hora

        db_contrato = ContratoORM(
            id=str(uuid.uuid4()),
            cliente_id=contrato.cliente_id,
            vehiculo_id=contrato.vehiculo_id,
            horas_contratadas=contrato.horas_contratadas,
            precio_por_hora=contrato.precio_por_hora,
            precio_total=precio_total,
            pagado=contrato.pagado,
            fecha_inicio=contrato.fecha_inicio,
            fecha_fin_estimada=contrato.fecha_fin_estimada,
            fecha_fin_real=contrato.fecha_fin_real,
            id_usuario_creacion=contrato.id_usuario_creacion
        )

        vehiculo.disponible = False
        db.add(db_contrato)
        db.commit()
        db.refresh(db_contrato)
        return db_contrato
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear contrato: {str(e)}")

@router.get("/", response_model=List[Contrato])
def listar_contratos(db: Session = Depends(get_db)):
    try:
        contratos = db.query(ContratoORM).order_by(ContratoORM.fecha_creacion.desc()).all()
        return contratos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar contratos: {str(e)}")

@router.get("/{contrato_id}", response_model=Contrato)
def obtener_contrato(contrato_id: str, db: Session = Depends(get_db)):
    contrato = db.query(ContratoORM).filter(ContratoORM.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return contrato

@router.put("/{contrato_id}", response_model=Contrato)
def actualizar_contrato(contrato_id: str, contrato: ContratoUpdate, db: Session = Depends(get_db)):
    try:
        db_contrato = db.query(ContratoORM).filter(ContratoORM.id == contrato_id).first()
        if not db_contrato:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")
        cliente = db.query(ClienteORM).filter(ClienteORM.id == contrato.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == contrato.vehiculo_id).first()
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        db_contrato.cliente_id = contrato.cliente_id
        db_contrato.vehiculo_id = contrato.vehiculo_id
        db_contrato.horas_contratadas = contrato.horas_contratadas
        db_contrato.precio_por_hora = contrato.precio_por_hora
        db_contrato.precio_total = contrato.horas_contratadas * contrato.precio_por_hora
        db_contrato.pagado = contrato.pagado
        db_contrato.fecha_inicio = contrato.fecha_inicio
        db_contrato.fecha_fin_estimada = contrato.fecha_fin_estimada
        db_contrato.fecha_fin_real = contrato.fecha_fin_real
        db_contrato.fecha_actualizacion = datetime.now()
        db_contrato.id_usuario_edicion = contrato.id_usuario_edicion

        db.commit()
        db.refresh(db_contrato)
        return db_contrato
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar contrato: {str(e)}")

@router.delete("/{contrato_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contrato(contrato_id: str, db: Session = Depends(get_db)):
    try:
        db_contrato = db.query(ContratoORM).filter(ContratoORM.id == contrato_id).first()
        if not db_contrato:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")
        vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == db_contrato.vehiculo_id).first()
        if vehiculo:
            vehiculo.disponible = True
        db.delete(db_contrato)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar contrato: {str(e)}")
