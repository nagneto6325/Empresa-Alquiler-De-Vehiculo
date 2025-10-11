"""Módulo de controladores para la gestión de pagos en el sistema de alquiler de vehículos."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from database import SessionLocal
from app.models.orm.Pago import Pago as PagoORM
from app.models.orm.Contrato import Contrato as ContratoORM
from app.models.orm.Cliente import Cliente as ClienteORM

router = APIRouter()


def get_db():
    """Proporciona una sesión de base de datos y garantiza su cierre al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PagoBase(BaseModel):
    """Modelo base que define los campos principales de un pago."""

    contrato_id: str
    cliente_id: str
    monto: float
    metodo_pago: str = "Efectivo"
    fecha_pago: datetime
    estado: str = "Completado"
    id_usuario_creacion: Optional[str] = None


class PagoCreate(PagoBase):
    """Modelo utilizado para la creación de un nuevo pago."""

    pass


class PagoUpdate(PagoBase):
    """Modelo utilizado para la actualización de un pago existente."""

    id_usuario_edicion: Optional[str] = None


class Pago(BaseModel):
    """Modelo de respuesta que representa un pago completo en el sistema."""

    id: str
    contrato_id: str
    cliente_id: str
    monto: float
    metodo_pago: str
    fecha_pago: datetime
    estado: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario_creacion: Optional[str] = None
    id_usuario_edicion: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=Pago)
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo registro de pago y actualiza el estado del contrato si aplica."""
    try:
        contrato = db.query(ContratoORM).filter(ContratoORM.id == pago.contrato_id).first()
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")

        cliente = db.query(ClienteORM).filter(ClienteORM.id == pago.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db_pago = PagoORM(
            id=str(uuid.uuid4()),
            contrato_id=pago.contrato_id,
            cliente_id=pago.cliente_id,
            monto=pago.monto,
            metodo_pago=pago.metodo_pago,
            fecha_pago=pago.fecha_pago,
            estado=pago.estado,
            id_usuario_creacion=pago.id_usuario_creacion,
        )

        if pago.estado == "Completado":
            contrato.pagado = True

        db.add(db_pago)
        db.commit()
        db.refresh(db_pago)
        return db_pago

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear pago: {str(e)}")


@router.get("/", response_model=List[Pago])
def listar_pagos(db: Session = Depends(get_db)):
    """Obtiene una lista con todos los pagos registrados en el sistema."""
    try:
        pagos = db.query(PagoORM).order_by(PagoORM.fecha_creacion.desc()).all()
        return pagos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar pagos: {str(e)}")


@router.get("/{pago_id}", response_model=Pago)
def obtener_pago(pago_id: str, db: Session = Depends(get_db)):
    """Obtiene un pago específico mediante su identificador único."""
    pago = db.query(PagoORM).filter(PagoORM.id == pago_id).first()
    if pago is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


@router.put("/{pago_id}", response_model=Pago)
def actualizar_pago(pago_id: str, pago: PagoUpdate, db: Session = Depends(get_db)):
    """Actualiza la información de un pago existente."""
    try:
        db_pago = db.query(PagoORM).filter(PagoORM.id == pago_id).first()
        if db_pago is None:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        contrato = db.query(ContratoORM).filter(ContratoORM.id == pago.contrato_id).first()
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")

        cliente = db.query(ClienteORM).filter(ClienteORM.id == pago.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db_pago.contrato_id = pago.contrato_id
        db_pago.cliente_id = pago.cliente_id
        db_pago.monto = pago.monto
        db_pago.metodo_pago = pago.metodo_pago
        db_pago.fecha_pago = pago.fecha_pago
        db_pago.estado = pago.estado
        db_pago.id_usuario_edicion = pago.id_usuario_edicion

        if pago.estado == "Completado":
            contrato.pagado = True
        else:
            contrato.pagado = False

        db.commit()
        db.refresh(db_pago)
        return db_pago

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar pago: {str(e)}")


@router.delete("/{pago_id}")
def eliminar_pago(pago_id: str, db: Session = Depends(get_db)):
    """Elimina un registro de pago y actualiza el estado del contrato relacionado."""
    try:
        db_pago = db.query(PagoORM).filter(PagoORM.id == pago_id).first()
        if db_pago is None:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        contrato = db.query(ContratoORM).filter(ContratoORM.id == db_pago.contrato_id).first()
        if contrato:
            contrato.pagado = False

        db.delete(db_pago)
        db.commit()
        return {"message": "Pago eliminado correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar pago: {str(e)}")
