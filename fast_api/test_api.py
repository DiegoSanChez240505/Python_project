from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from fast_api.conection import SessionLocal
from sqlalchemy import text
import pickle
from pathlib import Path

app = FastAPI(
    title="Test API",
    description="Simple test API to diagnose server issues",
    version="1.0.0"
)

# Cargar modelos de IA si existen
modelo = None
model2 = None

try:
    modelo_path = Path(r"C:\Python_project\modelo_entrenado.pkl")
    if modelo_path.exists():
        with open(modelo_path, "rb") as file:
            modelo = pickle.load(file)
            
    modelo_path2 = Path(r"C:\Python_project\modelo_monto_pago.pkl")
    if modelo_path2.exists():
        with open(modelo_path2, "rb") as file:
            model2 = pickle.load(file)
except Exception as e:
    print(f"Error al cargar modelos: {e}")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="fast_api/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="fast_api/templates")

# Rutas para las páginas HTML
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict-page", response_class=HTMLResponse)
def predict_page(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.get("/payment-page", response_class=HTMLResponse)
def payment_page(request: Request):
    return templates.TemplateResponse("predict_payment.html", {"request": request})

# Rutas para las APIs de prueba
@app.get("/api/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/api/test")
def test():
    return {"status": "OK", "message": "Test endpoint is working"}

# Rutas para las APIs de predicción
@app.get("/predict")
def predict(db: Session = Depends(get_db)):
    try:
        if modelo is None:
            return {"error": "Modelo no cargado"}
            
        # Verificar conexión
        db.execute(text("SELECT 1"))
        
        # Consultar datos
        query = text("SELECT amount, refunded_amount FROM transactions") 
        result = db.execute(query)
        rows = result.fetchall()
        
        if not rows:
            return {"message": "No hay datos para predecir"}
            
        # Convertir a DataFrame
        df = pd.DataFrame(rows, columns=["amount", "refunded_amount"])
        
        # Preparar datos para la predicción
        X = np.array(df[['amount', 'refunded_amount']].astype(float))
        
        # Hacer predicción
        predicciones = modelo.predict(X)
        return {"predicciones": predicciones.tolist()}
    except Exception as e:
        return {"error": f"Error en la predicción: {str(e)}"}

@app.get("/predict_payment/")
def predict_payment(user_id: str, db: Session = Depends(get_db)):
    try:
        if model2 is None:
            return {"error": "Modelo de pago no cargado"}
            
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
        expected_features = model2.feature_names_in_
        input_data = input_data[expected_features]
    
        prediction = model2.predict(input_data)
    
        return {"user_id": user_id, "predicted_amount": round(float(prediction[0]), 2)}
    except Exception as e:
        return {"error": f"Error en la predicción de pago: {str(e)}"}