import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="keidot_db",
            user="diego_sanchez",
            password="Dase@081204",
            host="keidot.postgres.database.azure.com",  # Cambia si usas un servidor remoto
            port="5432"  # Puerto por defecto de PostgreSQL
        )
        print("✅ Conexión exitosa a PostgreSQL")
        return conn
    except Exception as e:
        print(f"⚠️ Error al conectar: {e}")
        return None

# Prueba la conexión
if __name__ == "__main__":
    connect_db()
