import joblib
import numpy as np
import pandas as pd
import shap
import matplotlib
matplotlib.use('Agg')  # Backend para entornos sin interfaz gráfica
import matplotlib.pyplot as plt
import os
from tensorflow.keras.models import load_model


MODEL_PATH = "best_ann.keras"
PREPROCESSOR_PATH = "preprocessor.pkl"

# Cargar modelo y preprocesador globalmente
MODEL = load_model(MODEL_PATH)
MODEL.trainable = False
for layer in MODEL.layers:
    layer.trainable = False

PREPROCESSOR = joblib.load(PREPROCESSOR_PATH)
BACKGROUND_DATA = joblib.load("background_data.pkl")
EXPLAINER = shap.Explainer(MODEL, BACKGROUND_DATA, framework='tensorflow')

# Configuración de columnas
CATEGORICAL_FEATURES = [
    "gender", "hypertension", "heart_disease", "ever_married",
    "work_type", "Residence_type", "smoking_status"
]
NUMERICAL_FEATURES = ["age", "avg_glucose_level", "bmi"]


def get_reverted_shap_explanation(person_data):
    """
    Combina la generación de valores SHAP y la reversión de los datos
    transformados. Devuelve un objeto shap.Explanation cuyas 'data' y
    'feature_names' coinciden con los valores originales (edad=30.0,
    etc.) en lugar de los datos escalados/one-hot.

    Args:
        person_data (dict): Diccionario con las claves:
            ['age', 'avg_glucose_level', 'bmi', 'gender', 'hypertension',
             'heart_disease', 'ever_married', 'work_type',
             'Residence_type', 'smoking_status']

    Returns:
        shap.Explanation: Objeto con .data, .base_values, .values,
        .feature_names (con los datos desescalados y revertidos de su nombre
        ‘one-hot’).
    """
    # Generar shap_values con EXPLAINER
    df = pd.DataFrame([person_data])[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    transformed_data = PREPROCESSOR.transform(df)
    shap_values = EXPLAINER(transformed_data)

    # Revertir valores numéricos en shap_values.data a escala original
    data_reverted = shap_values.data.copy()
    scaler = PREPROCESSOR.named_transformers_['num']
    data_reverted[:, :len(NUMERICAL_FEATURES)] = (
            data_reverted[:, :len(NUMERICAL_FEATURES)] * scaler.scale_
            + scaler.mean_
    )

    # Actualizar los feature_names
    encoder = PREPROCESSOR.named_transformers_['cat']
    onehot_feature_names = encoder.get_feature_names_out(CATEGORICAL_FEATURES)
    feature_names_reverted = list(NUMERICAL_FEATURES) + list(
        onehot_feature_names)

    shap_values.data = data_reverted
    shap_values.feature_names = feature_names_reverted

    return shap_values


def get_force_plot(shap_explanation):
    # Con show=False y matplotlib=True, fuerza a SHAP a generar una figura
    # Matplotlib
    shap.plots.force(shap_explanation.base_values[0],
                     shap_explanation.values[0],
                     feature_names=shap_explanation.feature_names,
                     matplotlib=True,
                     show=False)
    fig = plt.gcf()
    return fig


def get_waterfall_plot(shap_explanation, max_display=10):
    """
    Genera un SHAP waterfall plot y retorna la figura de matplotlib.
    """
    shap.plots.waterfall(shap_explanation[0],
                         max_display=max_display,
                         show=True)
    fig = plt.gcf()
    return fig


def get_decision_plot(shap_explanation):
    """
    Genera un decision plot de SHAP.
    """
    shap.decision_plot(shap_explanation.base_values[0],
                       shap_explanation.values[0],
                       shap_explanation.feature_names,
                       show=False)
    fig = plt.gcf()
    return fig
