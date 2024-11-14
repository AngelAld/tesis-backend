from IA.models import ModeloIA
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import tensorflow as tf


def identificar_tipo_modelo(modelo: ModeloIA):
    if modelo.archivo.name.endswith(".keras"):
        return "tf"
    elif modelo.archivo.name.endswith(".pkl"):
        return "sklearn"


def predecir(modelo: ModeloIA, datos: list):
    scaler = joblib.load(modelo.scaler.path)

    tipo_modelo = identificar_tipo_modelo(modelo)

    new_data = np.array([datos])

    new_data_scaled = scaler.transform(new_data)

    if tipo_modelo == "sklearn":
        linear_model = joblib.load(modelo.archivo.path)
        predicted_value = linear_model.predict(new_data_scaled)
        return predicted_value[0]
    elif tipo_modelo == "tf":
        nn_model = tf.keras.models.load_model(modelo.archivo.path)  # type: ignore
        predicted_value_nn = nn_model.predict(new_data_scaled).flatten()
        return predicted_value_nn[0]
    else:
        raise ValueError("Modelo no soportado")
