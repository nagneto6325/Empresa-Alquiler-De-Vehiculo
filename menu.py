"""
Módulo de menú interactivo y login de usuarios.
""" 
from database import SessionLocal, engine, Base
from .app.models.orm import Usuario, VehiculoORM, ClienteORM

Base.metadata.create_all(bind=engine)

def registrar_usuario():
    db = SessionLocal()
    username = input("Ingrese nombre de usuario: ")
    password = input("Ingrese contraseña: ")
    usuario = Usuario(username=username, password=password)
    db.add(usuario)
    db.commit()
    print("Usuario registrado con éxito!")
    db.close()

def login():
    db = SessionLocal()
    username = input("Usuario: ")
    password = input("Contraseña: ")
    usuario = db.query(Usuario).filter_by(username=username, password=password).first()
    db.close()
    if usuario:
        print(f"Bienvenido {usuario.username}")
        return True
    else:
        print("Credenciales inválidas")
        return False

def menu():
    while True:
        print("\n--- Sistema de Alquiler ---")
        print("1. Registrar usuario")
        print("2. Login")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            if login():
                print("Acceso concedido")
        elif opcion == "3":
            break
        else:
            print("Opción no válida")
