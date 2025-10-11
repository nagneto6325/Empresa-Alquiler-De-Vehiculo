"""Servicios para autenticación y autorización."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import jwt
from app.models.orm.Usuario import Usuario
from app.models.orm.Cliente import Cliente
from utils.auth import SECRET_KEY, ALGORITHM

class AuthService:
    """Servicio para operaciones de autenticación."""
    
    @staticmethod
    def autenticar_usuario(db: Session, username: str, password: str) -> dict:
        """Autenticar usuario y generar token."""
        usuario = db.query(Usuario).filter(
            Usuario.username == username,
            Usuario.password == password  # En producción: verificar hash
        ).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        # Obtener cliente asociado
        cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario.id).first()
        
        # Generar token
        token_data = {
            "sub": usuario.username,
            "user_id": usuario.id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "username": usuario.username
            },
            "cliente": cliente
        }
    
    @staticmethod
    def registrar_usuario(db: Session, username: str, password: str) -> dict:
        """Registrar nuevo usuario y cliente asociado."""
        from app.models.services.usuario_services import UsuarioService
        return UsuarioService.crear_usuario_completo(db, username, password)
    
    @staticmethod
    def verificar_token(token: str) -> dict:
        """Verificar y decodificar token JWT."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )