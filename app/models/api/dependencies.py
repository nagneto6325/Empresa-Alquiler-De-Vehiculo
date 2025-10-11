"""Dependencias compartidas para la API."""

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator
from database import SessionLocal
from utils.auth import obtener_usuario_actual
from app.models.orm.Usuario import Usuario

def get_db() -> Generator[Session, None, None]:
    """Dependency para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    current_user: Usuario = Depends(obtener_usuario_actual)
) -> Usuario:
    """Dependency para obtener usuario actual."""
    return current_user