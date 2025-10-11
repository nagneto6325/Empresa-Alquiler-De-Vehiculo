"""Configuración simplificada de la base de datos."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///alquiler_vehiculos.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Crea las tablas del modelo ORM sin insertar datos iniciales."""
    from app.models.orm.Usuario import Usuario
    from app.models.orm.Cliente import Cliente
    from app.models.orm.Vehiculo import Vehiculo
    from app.models.orm.Contrato import Contrato
    from app.models.orm.Pago import Pago
    from app.models.orm.Mantenimiento import Mantenimiento

    try:
        print("Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas correctamente.")
        tablas = Base.metadata.tables.keys()
        print(f"Tablas creadas: {list(tablas)}")
    except Exception as e:
        print(f"Error creando tablas: {e}")
        import traceback

        traceback.print_exc()


def get_db():
    """Genera y gestiona una sesión de base de datos SQLAlchemy."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    """Ejecuta la inicialización de la base de datos si se ejecuta directamente."""
    init_db()
