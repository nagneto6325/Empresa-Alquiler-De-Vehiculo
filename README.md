Sistema de Alquiler de Vehículos

Este proyecto es una aplicación de consola para la gestión de un sistema de alquiler de vehículos.  
Permite gestionar clientes, vehículos, contratos, pagos y mantenimientos, con control de usuarios y autenticación básica.

---

📂 Estructura del proyecto

proyecto_alquiler/
├── app/
│   ├── models/orm/         Modelos ORM con SQLAlchemy
│   ├── sistema_alquiler.py Lógica principal del sistema
│
├── utils/
│   └── auth.py             Módulo de autenticación (login)
│
├── database.py              Configuración de la base de datos
├── menu.py                  Menú interactivo
├── main.py                  Punto de entrada principal
├── requirements.txt         Dependencias del proyecto
└── README.md                Este archivo

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

