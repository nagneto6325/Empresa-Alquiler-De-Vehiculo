"""Endpoints para la gestión de clientes en la API del sistema de alquiler."""

import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from app.models.orm.Cliente import Cliente as ClienteORM
from app.models.schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter()


def get_db():
    """Proporciona una sesión de base de datos y garantiza su cierre al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ClienteResponse, summary="Crear cliente")
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crea un nuevo cliente en el sistema utilizando un identificador UUID único."""
    try:
        db_cliente = ClienteORM(
            id=str(uuid.uuid4()),
            nombre=cliente.nombre,
            contacto=cliente.contacto,
            usuario_id=cliente.usuario_id,
            id_usuario_creacion="sistema",
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear cliente: {str(e)}")


@router.get("/", response_model=list[ClienteResponse], summary="Listar clientes")
def listar_clientes(db: Session = Depends(get_db)):
    """Obtiene la lista completa de clientes registrados, ordenados por fecha de creación."""
    try:
        clientes = db.query(ClienteORM).order_by(ClienteORM.fecha_creacion.desc()).all()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar clientes: {str(e)}")


@router.get("/{cliente_id}", response_model=ClienteResponse, summary="Obtener cliente")
def obtener_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Obtiene la información de un cliente específico mediante su identificador UUID."""
    cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse, summary="Actualizar cliente")
def actualizar_cliente(cliente_id: str, cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Actualiza los datos de un cliente existente utilizando su identificador UUID."""
    try:
        db_cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db_cliente.nombre = cliente.nombre
        db_cliente.contacto = cliente.contacto
        db_cliente.usuario_id = cliente.usuario_id
        db_cliente.id_usuario_edicion = "sistema"

        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar cliente: {str(e)}")


@router.delete("/{cliente_id}", summary="Eliminar cliente")
def eliminar_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Elimina un cliente del sistema mediante su identificador UUID."""
    try:
        db_cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db.delete(db_cliente)
        db.commit()
        return {"message": "Cliente eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {str(e)}")
