"""Punto de entrada principal del sistema de alquiler.

Este modulo gestiona la autenticacion de usuarios y el menu principal
del sistema de alquiler de vehiculos. Proporciona funcionalidades
de registro, login y navegacion al sistema principal.
"""

from database import init_db, SessionLocal
from app.models.orm.Usuario import Usuario
from app.models.orm.Cliente import Cliente
from app.sistema_alquiler import SistemaAlquiler


def registrar_usuario(username, password):
    """Registra un nuevo usuario en el sistema.
    
    Args:
        username (str): Nombre de usuario para el registro
        password (str): Contrasena para el nuevo usuario
        
    Returns:
        bool: True si el registro fue exitoso, False en caso contrario
        
    Raises:
        Exception: Si ocurre un error durante el proceso de registro
    """
    db = SessionLocal()
    try:
        usuario_existente = db.query(Usuario).filter_by(username=username).first()
        if usuario_existente:
            print("El usuario ya existe.")
            return False

        nuevo_usuario = Usuario(
            username=username,
            password=password,
            id_usuario_creacion="sistema",
        )
        db.add(nuevo_usuario)
        db.commit()

        nuevo_cliente = Cliente(
            nombre=username,
            usuario_id=nuevo_usuario.id,
            id_usuario_creacion="sistema",
        )
        db.add(nuevo_cliente)
        db.commit()

        print("Usuario registrado con exito!")
        return True

    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def login(username, password):
    """Autentica un usuario y devuelve el cliente asociado.
    
    Args:
        username (str): Nombre de usuario para autenticar
        password (str): Contrasena del usuario
        
    Returns:
        tuple: Tupla con (cliente, usuario_id) si la autenticacion es exitosa,
               (None, None) en caso contrario
               
    Raises:
        Exception: Si ocurre un error durante el proceso de autenticacion
    """
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(username=username, password=password).first()
        if usuario:
            cliente = db.query(Cliente).filter_by(usuario_id=usuario.id).first()
            if cliente:
                print(f"Bienvenido {usuario.username}!")
                return cliente, usuario.id
        print("Credenciales invalidas")
        return None, None
    except Exception as e:
        print(f"Error en login: {e}")
        return None, None
    finally:
        db.close()


def main():
    """Funcion principal del sistema.
    
    Gestiona el flujo principal de la aplicacion incluyendo:
    - Inicializacion de la base de datos
    - Presentacion del menu principal
    - Manejo de opciones del usuario
    - Navegacion entre diferentes funcionalidades
    """
    print("=" * 50)
    print("SISTEMA DE ALQUILER DE VEHICULOS")
    print("=" * 50)

    init_db()

    while True:
        print("\n" + "=" * 30)
        print("MENU PRINCIPAL")
        print("=" * 30)
        print("1. Login")
        print("2. Registrar usuario")
        print("3. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            print("\n--- INICIAR SESION ---")
            username = input("Usuario: ").strip()
            password = input("Contrasena: ").strip()

            cliente, usuario_id = login(username, password)
            if cliente and usuario_id:
                sistema = SistemaAlquiler(cliente, usuario_id)
                sistema.menu_principal()

        elif opcion == "2":
            print("\n--- REGISTRAR USUARIO ---")
            username = input("Nuevo usuario: ").strip()
            password = input("Contrasena: ").strip()

            if len(username) < 3:
                print("El usuario debe tener al menos 3 caracteres")
                continue
            if len(password) < 3:
                print("La contrasena debe tener al menos 3 caracteres")
                continue

            registrar_usuario(username, password)

        elif opcion == "3":
            print("\nGracias por usar el sistema!")
            break

        else:
            print("Opcion no valida. Intente nuevamente.")


if __name__ == "__main__":
    """Punto de ejecucion principal cuando el script se ejecuta directamente."""
    main()