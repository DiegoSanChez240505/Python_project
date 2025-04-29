from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fast_api.conection import SessionLocal  # Importamos la sesión correctamente
import pickle
import numpy as np
import pandas as pd  
from pathlib import Path
from sqlalchemy import text
from datetime import datetime
from dateutil import parser

app = FastAPI(
    title="Mi API", 
    description="API para predicciones", 
    version="1.0.0", 
    docs_url="/docs",  # Asegura que Swagger está habilitado
    redoc_url="/redoc"
)

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="fast_api/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="fast_api/templates")

# Cargar modelo de IA previamente entrenado
modelo_path = Path(r"C:\Python_project\modelo_entrenado.pkl")
if not modelo_path.exists():
    raise FileNotFoundError(f"No se encontró el modelo en {modelo_path}")

with open(modelo_path, "rb") as file:
    modelo = pickle.load(file)

modelo_path2 = Path(r"C:\Python_project\modelo_monto_pago.pkl")
if not modelo_path2.exists():
    raise FileNotFoundError(f"No se encontró el modelo en {modelo_path2}")

with open(modelo_path2, "rb") as file:
    model2 = pickle.load(file)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas para las páginas web
@app.get("/")
def root(request: Request):
    # Redirigir a la página de login como página principal
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
def dashboard(request: Request):
    # Esta era la antigua ruta principal, ahora es dashboard y requiere login
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict-page")
def predict_page(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.get("/payment-page")
def payment_page(request: Request):
    return templates.TemplateResponse("predict_payment.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Ruta API para información básica
@app.get("/api/info")
def api_info():
    return {"message": "API de IA con PostgreSQL"}

@app.get("/predict")
def predict(db: Session = Depends(get_db)):
    try:
        # Verificar conexión
        db.execute(text("SELECT 1"))
        print("✅ Conexión a PostgreSQL exitosa")
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")
        return {"error": f"No se pudo conectar a la base de datos. Detalles: {str(e)}"}

    # 🔹 Asegúrate de seleccionar 2 columnas que correspondan al modelo
    query = text("SELECT amount, refunded_amount FROM transactions") 

    try:
        # Ejecutar la consulta con SQLAlchemy
        result = db.execute(query)
        rows = result.fetchall()

        if not rows:
            return {"message": "No hay datos para predecir"}

        # Convertir a DataFrame
        df = pd.DataFrame(rows, columns=["amount", "refunded_amount"])
        print(f"✅ Datos obtenidos: {df.shape}")
    except Exception as e:
        print(f"❌ Error al ejecutar la consulta SQL: {e}")
        return {"error": "Error al obtener datos de la base de datos"}

    # Preparar datos para la predicción (deben ser 2 columnas)
    X = np.array(df[['amount', 'refunded_amount']].astype(float))


    print(f"✅ Datos preparados para la predicción: {X.shape}")

    try:
        print("🤖 Modelo haciendo predicciones...")
        print("🔍 Datos enviados al modelo:", X)
        predicciones = modelo.predict(X)
        print("✅ Predicción completada")
        return {"predicciones": predicciones.tolist()}
    except Exception as e:
        print(f"❌ Error al hacer la predicción: {e}")
        return {"error": "Error al procesar la predicción"}
    


@app.get("/predict_payment/")
def predict_payment(user_id: str, db: Session = Depends(get_db)):
    query = text("SELECT transaction_date FROM transactions WHERE id_user = :user_id ORDER BY transaction_date DESC LIMIT 1")
    result = db.execute(query, {"user_id": user_id}).fetchone()
    
    if not result:
        return {"error": "No se encontraron transacciones para este usuario"}

    last_transaction = result[0]

    input_data = pd.DataFrame([{
        "year": last_transaction.year,
        "month": last_transaction.month,
        "day": last_transaction.day,
        "hour": last_transaction.hour,
        "weekday": last_transaction.weekday()
    }])

    # Asegurar que las columnas coincidan con las usadas en el entrenamiento
    expected_features = model2.feature_names_in_  # Lista de nombres usados al entrenar
    input_data = input_data[expected_features]  # Filtrar solo las columnas correctas

    prediction = model2.predict(input_data)

    return {"user_id": user_id, "predicted_amount": round(float(prediction[0]), 2)}


# Código para iniciar el servidor si se ejecuta directamente este archivo
if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI...")
    print("La aplicación estará disponible en: http://127.0.0.1:8000")
    print("Presiona CTRL+C para detener el servidor")
    uvicorn.run(app, host="127.0.0.1", port=8000)
