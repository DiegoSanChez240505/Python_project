import numpy as np
import pickle  # o import pickle si usaste pickle

# Cargar el modelo
with open("modelo_entrenado.pkl", "rb") as f:
    model = pickle.load(f)  # Cargar el modelo desde el archivo .pkl

# Datos de prueba
nueva_transaccion = np.array([[50.00, 0.00]])  # Monto y monto reembolsado

# Asegúrate de que la entrada tenga la forma correcta

print("Forma de la entrada antes de predecir:", np.array(nueva_transaccion).shape)

# Hacer la predicción
prediccion = model.predict([nueva_transaccion]) # Asegúrate de que la entrada tenga la forma correcta
print("Predicción:", prediccion)
