"""Servicios para la gestión de usuarios."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.orm.Usuario import Usuario
from app.models.orm.Cliente import Cliente
from app.models.schemas.usuario import UsuarioCreate

class UsuarioService:
    """Servicio para operaciones de usuario."""
    
    @staticmethod
    def crear_usuario_completo(db: Session, usuario_data: UsuarioCreate) -> dict:
        """Crear usuario y cliente asociado."""
        # Verificar si el usuario ya existe
        usuario_existente = db.query(Usuario).filter(
            Usuario.username == usuario_data.username
        ).first()
        
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )
        
        # Crear usuario
        usuario = Usuario(
            username=usuario_data.username,
            password=usuario_data.password,  # En producción: hashear
            id_usuario_creacion="sistema"
        )
        db.add(usuario)
        db.flush()  # Para obtener el ID sin commit
        
        # Crear cliente automáticamente
        cliente = Cliente(
            nombre=usuario_data.username,
            usuario_id=usuario.id,
            id_usuario_creacion="sistema"
        )
        db.add(cliente)
        db.commit()
        db.refresh(usuario)
        db.refresh(cliente)
        
        return {
            "usuario": usuario,
            "cliente": cliente
        }
    
    @staticmethod
    def obtener_usuario_por_id(db: Session, usuario_id: str) -> Optional[Usuario]:
        """Obtener usuario por ID."""
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def listar_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Listar usuarios con paginación."""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar_usuario(db: Session, usuario_id: str, usuario_data: UsuarioCreate) -> Usuario:
        """Actualizar usuario existente."""
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar username único (excluyendo el actual)
        if usuario_data.username != usuario.username:
            existente = db.query(Usuario).filter(
                Usuario.username == usuario_data.username,
                Usuario.id != usuario_id
            ).first()
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está en uso"
                )
        
        usuario.username = usuario_data.username
        usuario.password = usuario_data.password
        usuario.id_usuario_edicion = "sistema"
        
        db.commit()
        db.refresh(usuario)
        return usuario
    
    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: str) -> bool:
        """Eliminar usuario y su cliente asociado."""
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Eliminar cliente asociado primero
        cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
        if cliente:
            db.delete(cliente)
        
        db.delete(usuario)
        db.commit()
        return True