"""Endpoints de autenticación para la API."""

import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from app.models.schemas.auth import UserRegister, Token
from app.models.orm.Usuario import Usuario as UsuarioORM

router = APIRouter(tags=["Autenticación"])


def get_db():
    """Crea una sesión de base de datos y asegura su cierre al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registrar", response_model=dict)
def registrar(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en la base de datos."""
    if len(user_data.username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario debe tener al menos 3 caracteres",
        )
    if len(user_data.password) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 3 caracteres",
        )

    existing_user = (
        db.query(UsuarioORM).filter(UsuarioORM.username == user_data.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )

    try:
        db_usuario = UsuarioORM(
            id=str(uuid.uuid4()),
            username=user_data.username,
            password=user_data.password,
            id_usuario_creacion="sistema",
        )

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)

        return {
            "message": "Usuario registrado con éxito",
            "usuario_id": db_usuario.id,
            "username": db_usuario.username,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}",
        )


@router.post("/login", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Permite iniciar sesión y obtener un token simulado de autenticación."""
    usuario = (
        db.query(UsuarioORM)
        .filter(
            UsuarioORM.username == form_data.username,
            UsuarioORM.password == form_data.password,
        )
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    return {
        "message": "Login exitoso",
        "access_token": f"token-{usuario.id}",
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "username": usuario.username,
            "fecha_creacion": usuario.fecha_creacion,
        },
    }


@router.get("/me")
def obtener_usuario_actual_endpoint(db: Session = Depends(get_db)):
    """Obtiene la información del primer usuario registrado como prueba."""
    usuario = db.query(UsuarioORM).first()
    if usuario:
        return {
            "id": usuario.id,
            "username": usuario.username,
            "fecha_creacion": usuario.fecha_creacion,
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No hay usuarios en el sistema",
    )
