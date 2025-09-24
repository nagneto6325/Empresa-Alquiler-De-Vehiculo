"""Funciones de autenticación de usuarios: registro y login."""

from app.models.orm.Usuario import Usuario
from database import SessionLocal


def registrar_usuario(username: str, password: str):
    """Registra un nuevo usuario si no existe previamente."""
    session = SessionLocal()
    existente = session.query(Usuario).filter_by(username=username).first()
    if existente:
        print("El usuario ya existe.")
        session.close()
        return None

    nuevo = Usuario(username=username, password=password)
    session.add(nuevo)
    session.commit()
    session.close()
    print("Usuario registrado correctamente.")
    return nuevo


def login(username: str, password: str):
    """Valida las credenciales de un usuario y permite el acceso si son correctas."""
    session = SessionLocal()
    usuario = (
        session.query(Usuario)
        .filter_by(username=username, password=password)
        .first()
    )
    session.close()
    if usuario:
        print("Acceso concedido.")
        return usuario
    else:
        print("Usuario o contraseña incorrectos.")
        return None
