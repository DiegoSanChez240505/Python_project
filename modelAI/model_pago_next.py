import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 📌 Conectar a la base de datos

# Escapar caracteres especiales en la contraseña
password = "Dase%40081204"  # '@' -> '%40'

# URL de conexión corregida
DATABASE_URL = f"postgresql+psycopg2://diego_sanchez:{password}@keidot.postgres.database.azure.com:5432/keidot_db?sslmode=require"

engine = create_engine(DATABASE_URL)

# 📌 Obtener datos de transacciones
query = text("""
    SELECT id_user, amount, transaction_date
    FROM transactions
""")
df = pd.read_sql(query, engine)

df["id_user"] = df["id_user"].astype(str)

# Codificar id_user en valores numéricos
encoder = LabelEncoder()
df["id_user"] = encoder.fit_transform(df["id_user"])

# 📌 Obtener datos de transacciones

df = pd.read_sql(query, engine)

# 📌 Convertir la fecha en variables útiles
df["transaction_date"] = pd.to_datetime(df["transaction_date"])
df["year"] = df["transaction_date"].dt.year
df["month"] = df["transaction_date"].dt.month
df["day"] = df["transaction_date"].dt.day
df["hour"] = df["transaction_date"].dt.hour
df["weekday"] = df["transaction_date"].dt.weekday

# 📌 Seleccionar variables de entrada y salida
X = df[['id_user', 'year', 'month', 'day', 'hour', 'weekday']]
y = df['amount']

# 📌 Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 📌 Entrenar el modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📌 Guardar el modelo entrenado
with open("modelo_monto_pago.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Modelo entrenado y guardado exitosamente.")
