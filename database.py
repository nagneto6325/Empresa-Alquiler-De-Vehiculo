"""Configuracion de la base de datos con campos de auditoria estandarizados.

Este modulo proporciona la configuracion base para la conexion a la base de datos
y la inicializacion de todas las tablas del sistema de alquiler de vehiculos.
"""

from datetime import datetime
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///alquiler.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Crear todas las tablas si no existen e insertar datos iniciales.
    
    Esta funcion realiza las siguientes acciones:
    - Importa todos los modelos del sistema para registrar las tablas
    - Crea todas las tablas en la base de datos si no existen
    - Inserta datos de prueba de vehiculos si la base esta vacia
    - Maneja errores durante la inicializacion y realiza rollback si es necesario
    
    Raises:
        Exception: Si ocurre algun error durante la creacion de tablas o insercion de datos
    """
    from app.models.orm.Usuario import Usuario
    from app.models.orm.Cliente import Cliente
    from app.models.orm.Vehiculo import Vehiculo
    from app.models.orm.Contrato import Contrato
    from app.models.orm.Pago import Pago
    from app.models.orm.Mantenimiento import Mantenimiento

    Base.metadata.create_all(bind=engine)
    print("Todas las tablas creadas correctamente")

    db = SessionLocal()
    try:
        tablas = Base.metadata.tables.keys()
        print(f"Tablas creadas: {list(tablas)}")

        if db.query(Vehiculo).count() == 0:
            vehiculos_iniciales = [
                Vehiculo(
                    nombre="Toyota Corolla",
                    tipo="Auto",
                    tarifa_hora=25000,
                    puertas=4,
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Honda Civic",
                    tipo="Auto",
                    tarifa_hora=28000,
                    puertas=4,
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Yamaha R3",
                    tipo="Moto",
                    tarifa_hora=15000,
                    cilindraje=321,
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Suzuki GSX-R",
                    tipo="Moto",
                    tarifa_hora=18000,
                    cilindraje=600,
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Toyota Hilux",
                    tipo="Camioneta",
                    tarifa_hora=40000,
                    capacidad_carga=1000,
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Bicicleta Montana",
                    tipo="Bicicleta",
                    tarifa_hora=5000,
                    tipo_bici="montana",
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Bicicleta Urbana",
                    tipo="Bicicleta",
                    tarifa_hora=4000,
                    tipo_bici="urbana",
                    id_usuario_creacion="sistema",
                ),
                Vehiculo(
                    nombre="Patineta Xiaomi",
                    tipo="Patineta",
                    tarifa_hora=7000,
                    autonomia_km=30,
                    id_usuario_creacion="sistema",
                ),
            ]

            db.add_all(vehiculos_iniciales)
            db.commit()
            print("Base de datos inicializada con vehiculos de prueba")
        else:
            print("La base de datos ya contiene datos")

    except Exception as e:
        print(f"Error al inicializar BD: {e}")
        db.rollback()
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    """Punto de entrada para ejecutar la inicializacion de la base de datos."""
    init_db()