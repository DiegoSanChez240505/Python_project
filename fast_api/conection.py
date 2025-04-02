from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

# Escapar caracteres especiales en la contraseña
password = "Dase%40081204"  # '@' -> '%40'

# URL de conexión corregida
DATABASE_URL = f"postgresql+psycopg2://diego_sanchez:{password}@keidot.postgres.database.azure.com:5432/keidot_db?sslmode=require"

# Crear el motor de SQLAlchemy con pool_pre_ping para detectar desconexiones
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear sesión con SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Conexión directa con psycopg2
try:
    cnx = psycopg2.connect(
        user="diego_sanchez",
        password="Dase@081204",  # Aquí sí puedes dejarlo sin escape
        host="keidot.postgres.database.azure.com",
        port="5432",
        database="keidot_db",
        sslmode="require"  # Conexión segura en Azure
    )
    print("✅ Conexión exitosa a PostgreSQL en Azure")
except psycopg2.OperationalError as e:
    print(f"❌ Error de conexión: {e}")
except Exception as e:
    print(f"⚠️ Error inesperado: {e}")
