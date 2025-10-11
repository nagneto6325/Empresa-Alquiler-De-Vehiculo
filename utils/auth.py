"""Funciones de autenticación de usuarios: registro y login."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.orm.Usuario import Usuario
from database import SessionLocal

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def registrar_usuario(username: str, password: str):
    """Registra un nuevo usuario si no existe previamente."""
    session = SessionLocal()
    try:
        existente = session.query(Usuario).filter_by(username=username).first()
        if existente:
            print("El usuario ya existe.")
            return None

        nuevo = Usuario(username=username, password=password)
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        print("Usuario registrado correctamente.")
        return nuevo
    finally:
        session.close()

def login(username: str, password: str):
    """Valida las credenciales de un usuario y permite el acceso si son correctas."""
    session = SessionLocal()
    try:
        usuario = (
            session.query(Usuario)
            .filter_by(username=username, password=password)
            .first()
        )
        if usuario:
            print("Acceso concedido.")
            return usuario
        else:
            print("Usuario o contraseña incorrectos.")
            return None
    finally:
        session.close()

def login_api(username: str, password: str, db: Session):
    """Versión mejorada de login para la API."""
    usuario = db.query(Usuario).filter_by(username=username, password=password).first()
    if usuario:
        token = f"token_simple_{usuario.id}"
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "username": usuario.username
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

async def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency para obtener el usuario actual desde el token."""
    token = credentials.credentials
    
    # Versión simplificada - extraer ID del token
    if token.startswith("token_simple_"):
        usuario_id = token.replace("token_simple_", "")
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if usuario:
            print(f"Usuario autenticado: {usuario.username}")
            return usuario
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )