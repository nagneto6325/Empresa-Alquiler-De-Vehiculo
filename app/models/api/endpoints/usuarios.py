from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid

from database import SessionLocal
from app.models.orm.Usuario import Usuario as UsuarioORM
from app.models.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioResponse, summary="Crear usuario")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario en el sistema."""
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(UsuarioORM).filter(UsuarioORM.username == usuario.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username ya existe")
        
        # Crear nuevo usuario
        db_usuario = UsuarioORM(
            id=str(uuid.uuid4()),
            username=usuario.username,
            password=usuario.password,
            id_usuario_creacion="sistema"
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@router.get("/", response_model=list[UsuarioResponse], summary="Listar usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    """Obtener lista de todos los usuarios."""
    try:
        usuarios = db.query(UsuarioORM).order_by(UsuarioORM.fecha_creacion.desc()).all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar usuarios: {str(e)}")

@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Obtener usuario")
def obtener_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """Obtener un usuario específico por ID."""
    usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse, summary="Actualizar usuario")
def actualizar_usuario(usuario_id: str, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Actualizar información de un usuario existente."""
    try:
        db_usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        if db_usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar si el nuevo username ya existe
        existing_user = db.query(UsuarioORM).filter(
            UsuarioORM.username == usuario.username,
            UsuarioORM.id != usuario_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username ya existe")
        
        # Actualizar usuario
        db_usuario.username = usuario.username
        db_usuario.password = usuario.password
        db_usuario.id_usuario_edicion = "sistema"
        
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

@router.delete("/{usuario_id}", summary="Eliminar usuario")
def eliminar_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """Eliminar un usuario del sistema."""
    try:
        db_usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        if db_usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        db.delete(db_usuario)
        db.commit()
        
        return {"message": "Usuario eliminado correctamente"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")