import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Simulación de datos similares a tu base de datos
data = pd.DataFrame({
    "amount": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400],
    "refunded_amount": [0, 0, 50, 0, 100, 0, 200, 0, 300, 0, 400, 0, 500, 0],
    "label": [1, 0, 1, 0, 2, 0, 1, 0, 2, 0, 2, 0, 2, 0]  # Simulando clases
})

# Usar solo las 2 columnas relevantes
X = data[["amount", "refunded_amount"]].values
y = data["label"].values  # Etiqueta de clasificación

# Dividir en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar el modelo
accuracy = model.score(X_test, y_test)
print(f'✅ Precisión del modelo con datos de transacciones: {accuracy:.2f}')

# Guardar el modelo entrenado
with open("modelo_entrenado.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Modelo guardado exitosamente con datos de transacciones.")
