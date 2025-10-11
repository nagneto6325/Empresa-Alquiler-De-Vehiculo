"""Módulo de controladores para la gestión de vehículos en el sistema de alquiler."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid

from database import SessionLocal
from app.models.orm.Vehiculo import Vehiculo as VehiculoORM
from app.models.schemas.vehiculo import VehiculoCreate, VehiculoResponse

router = APIRouter()


def get_db():
    """Proporciona una sesión de base de datos y garantiza su cierre al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=VehiculoResponse, summary="Crear vehículo")
def crear_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo registro de vehículo en el sistema."""
    try:
        db_vehiculo = VehiculoORM(
            id=str(uuid.uuid4()),
            nombre=vehiculo.nombre,
            tipo=vehiculo.tipo,
            tarifa_hora=float(vehiculo.tarifa_hora),
            disponible=vehiculo.disponible,
            necesita_mantenimiento=vehiculo.necesita_mantenimiento,
            puertas=vehiculo.puertas,
            cilindraje=vehiculo.cilindraje,
            capacidad_carga=vehiculo.capacidad_carga,
            tipo_bici=vehiculo.tipo_bici,
            autonomia_km=vehiculo.autonomia_km,
            id_usuario_creacion="sistema",
        )
        db.add(db_vehiculo)
        db.commit()
        db.refresh(db_vehiculo)
        return db_vehiculo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear vehículo: {str(e)}")


@router.get("/", response_model=list[VehiculoResponse], summary="Listar vehículos")
def listar_vehiculos(db: Session = Depends(get_db)):
    """Obtiene la lista completa de vehículos registrados."""
    try:
        vehiculos = db.query(VehiculoORM).order_by(VehiculoORM.fecha_creacion.desc()).all()
        return vehiculos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar vehículos: {str(e)}")


@router.get("/{vehiculo_id}", response_model=VehiculoResponse, summary="Obtener vehículo")
def obtener_vehiculo(vehiculo_id: str, db: Session = Depends(get_db)):
    """Obtiene los datos de un vehículo específico mediante su identificador único."""
    vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == vehiculo_id).first()
    if vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo


@router.put("/{vehiculo_id}", response_model=VehiculoResponse, summary="Actualizar vehículo")
def actualizar_vehiculo(vehiculo_id: str, vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    """Actualiza los datos de un vehículo existente en la base de datos."""
    try:
        db_vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == vehiculo_id).first()
        if db_vehiculo is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        db_vehiculo.nombre = vehiculo.nombre
        db_vehiculo.tipo = vehiculo.tipo
        db_vehiculo.tarifa_hora = float(vehiculo.tarifa_hora)
        db_vehiculo.disponible = vehiculo.disponible
        db_vehiculo.necesita_mantenimiento = vehiculo.necesita_mantenimiento
        db_vehiculo.puertas = vehiculo.puertas
        db_vehiculo.cilindraje = vehiculo.cilindraje
        db_vehiculo.capacidad_carga = vehiculo.capacidad_carga
        db_vehiculo.tipo_bici = vehiculo.tipo_bici
        db_vehiculo.autonomia_km = vehiculo.autonomia_km
        db_vehiculo.id_usuario_edicion = "sistema"

        db.commit()
        db.refresh(db_vehiculo)
        return db_vehiculo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar vehículo: {str(e)}")


@router.delete("/{vehiculo_id}", summary="Eliminar vehículo")
def eliminar_vehiculo(vehiculo_id: str, db: Session = Depends(get_db)):
    """Elimina un vehículo del sistema mediante su identificador único."""
    try:
        db_vehiculo = db.query(VehiculoORM).filter(VehiculoORM.id == vehiculo_id).first()
        if db_vehiculo is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        db.delete(db_vehiculo)
        db.commit()
        return {"message": "Vehículo eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar vehículo: {str(e)}")
