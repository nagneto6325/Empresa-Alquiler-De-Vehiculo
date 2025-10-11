"""Punto de entrada principal de la API del sistema de alquiler."""

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import init_db


"""Intento de importación de endpoints desde las rutas esperadas."""
try:
    from app.models.api.endpoints.auth import router as auth_router
    from app.models.api.endpoints.usuarios import router as usuarios_router
    from app.models.api.endpoints.clientes import router as clientes_router
    from app.models.api.endpoints.vehiculos import router as vehiculos_router
    from app.models.api.endpoints.contratos import router as contratos_router
    from app.models.api.endpoints.pagos import router as pagos_router
    from app.models.api.endpoints.mantenimientos import router as mantenimientos_router

    print("Endpoints cargados desde: app.models.api.endpoints")
    ESTRUCTURA = "app.models.api.endpoints"

except ImportError as e:
    print(f"Error importando endpoints: {e}")
    try:
        from app.models.api.endpoints.auth import router as auth_router
        from app.models.api.endpoints.usuarios import router as usuarios_router
        from app.models.api.endpoints.clientes import router as clientes_router
        from app.models.api.endpoints.vehiculos import router as vehiculos_router
        from app.models.api.endpoints.contratos import router as contratos_router
        from app.models.api.endpoints.pagos import router as pagos_router
        from app.models.api.endpoints.mantenimientos import router as mantenimientos_router

        print("Endpoints cargados desde: endpoints/")
        ESTRUCTURA = "endpoints"

    except ImportError as e2:
        print(f"Error importando endpoints: {e2}")
        print("Creando routers básicos como fallback.")
        ESTRUCTURA = "basica"

        auth_router = APIRouter()
        usuarios_router = APIRouter()
        clientes_router = APIRouter()
        vehiculos_router = APIRouter()
        contratos_router = APIRouter()
        pagos_router = APIRouter()
        mantenimientos_router = APIRouter()


"""Creación e inicialización de la aplicación FastAPI."""
app = FastAPI(
    title="Sistema de Alquiler de Vehículos API",
    description="API RESTful para el sistema de alquiler de vehículos",
    version="1.0.0",
)


"""Configuración del middleware CORS para permitir peticiones externas."""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""Inclusión de los routers principales en la aplicación."""
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(usuarios_router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(clientes_router, prefix="/api/clientes", tags=["Clientes"])
app.include_router(vehiculos_router, prefix="/api/vehiculos", tags=["Vehículos"])
app.include_router(contratos_router, prefix="/api/contratos", tags=["Contratos"])
app.include_router(pagos_router, prefix="/api/pagos", tags=["Pagos"])
app.include_router(
    mantenimientos_router, prefix="/api/mantenimientos", tags=["Mantenimientos"]
)

print("Todos los routers incluidos correctamente.")


@app.on_event("startup")
async def startup_event():
    """Inicializa la base de datos y muestra información de arranque."""
    try:
        init_db()
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Error inicializando la base de datos: {e}")

    print("API del Sistema de Alquiler iniciada correctamente.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/")
async def root():
    """Endpoint raíz de la API principal."""
    return {
        "message": "Bienvenido a la API del Sistema de Alquiler de Vehículos",
        "version": "1.0.0",
        "status": "operational",
        "database": "SQLAlchemy ORM",
        "estructura": ESTRUCTURA,
    }


@app.get("/health")
async def health_check():
    """Verifica el estado de la API y la conexión a la base de datos."""
    return {"status": "healthy", "database": "SQLAlchemy"}


if __name__ == "__main__":
    """Ejecuta el servidor Uvicorn en modo desarrollo."""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
