Este proyecto es una aplicación qe corre en la web para la gestión de un sistema de alquiler de vehículos.  
Permite gestionar clientes, vehículos, contratos, pagos y mantenimientos, con control de usuarios y autenticación básica.

---

⚙️ Configuración

1. Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate   Linux/Mac
venv\Scripts\activate    Windows

2. Instalar dependencias
pip install -r requirements.txt

3. Configurar base de datos

Por defecto, el proyecto usa SQLite local (alquiler.db).  
Puedes migrar fácilmente a PostgreSQL/Neon configurando la variable de entorno:

export DATABASE_URL="postgresql+psycopg2://usuario:password@host:5432/nombre_db"

El archivo database.py leerá esta variable automáticamente.

---

▶️ Ejecución

Inicializa la base de datos y corre la aplicación con:

python main.py

El sistema mostrará un menú interactivo para:

- Registrar usuarios (login/registro)
- Administrar clientes
- Administrar vehículos
- Crear contratos
- Registrar pagos
- Registrar mantenimientos

---

🔐 Autenticación

- Los usuarios se registran y se validan con usuario/contraseña.  
- Se recomienda usar contraseñas seguras (con hashing mediante bcrypt).

---

📖 Lógica de negocio

1. Usuarios: se registran con credenciales y pueden autenticarse en el sistema.
2. Clientes: se registran y se asocian a contratos de alquiler.
3. Vehículos: se administran y se asocian a contratos.
4. Contratos: relacionan clientes y vehículos en un periodo de alquiler.
5. Pagos: se registran para contratos activos.
6. Mantenimientos: permiten llevar control del estado de los vehículos.

---

🚀 Nuevos Funcionamientos

El sistema fue ampliado con una **API RESTful completa** desarrollada con **FastAPI** y **SQLAlchemy**, que reemplaza el menú de consola tradicional.

Ahora incluye:

- **Ejecución con Uvicorn** (`python main.py` o `uvicorn main:app --reload`) para iniciar el servidor.
- **Rutas organizadas en módulos** dentro de la carpeta `app/models/api/endpoints`, separadas por entidad:
  - `/api/clientes`
  - `/api/vehiculos`
  - `/api/contratos`
  - `/api/pagos`
  - `/api/mantenimientos`
  - `/api/usuarios`
- **Conexión a base de datos SQLite o PostgreSQL**, configurable mediante variable de entorno.
- **Modelos ORM unificados con SQLAlchemy**, con control de auditoría (`fecha_creacion`, `fecha_actualizacion`, `id_usuario_creacion`, `id_usuario_edicion`).
- **Autenticación y control de usuarios** integrados en la API.
- **CORS habilitado** para permitir peticiones desde cualquier cliente.
- **Documentación interactiva** disponible en:
  - Swagger UI → http://localhost:8000/docs
- **Validaciones automáticas** con Pydantic y manejo de errores HTTP detallado.

Con estos cambios, el sistema puede utilizarse tanto desde una interfaz web como desde aplicaciones externas que consuman la API.
