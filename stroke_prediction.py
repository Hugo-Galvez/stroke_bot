import joblib
import pandas as pd
import re
import ast
# noinspection PyUnresolvedReferences
from tensorflow.keras.models import load_model

MODEL_PATH = "best_ann.keras"
PREPROCESSOR_PATH = "preprocessor.pkl"

# Cargar modelo y preprocesador globalmente
MODEL = load_model(MODEL_PATH)
MODEL.trainable = False
for layer in MODEL.layers:
    layer.trainable = False

PREPROCESSOR = joblib.load(PREPROCESSOR_PATH)

# Configuración de columnas
CATEGORICAL_FEATURES = [
    "gender", "hypertension", "heart_disease", "ever_married",
    "work_type", "Residence_type", "smoking_status"
]
NUMERICAL_FEATURES = ["age", "avg_glucose_level", "bmi"]


def extract_dictionary(response_text):
    """
    Extrae un diccionario de texto utilizando expresiones regulares.

    Args:
        response_text (str): Texto que contiene el diccionario.

    Returns:
        dict: Diccionario extraído si es válido.
        None: Si no se encuentra un diccionario válido.
    """
    try:
        match = re.search(r"\{.*?}", response_text, re.DOTALL)
        if match:
            extracted_dict = ast.literal_eval(match.group(0))
            if isinstance(extracted_dict, dict):
                return extracted_dict
    except Exception as e:
        print(f"Error al extraer el diccionario: {e}")
    return None


def validate_input(person_data):
    """
    Valida que los datos de entrada contengan todas las claves necesarias.

    Args:
        person_data (dict): Información de la persona.

    Raises:
        ValueError: Si faltan claves necesarias en los datos.
    """
    required_keys = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    missing_keys = [key for key in required_keys if key not in person_data]
    if missing_keys:
        raise ValueError(f"Faltan las claves necesarias: {missing_keys}")

    # Validación de variables categóricas
    for key in CATEGORICAL_FEATURES:
        if key == "gender" and person_data[key] not in ["Male", "Female"]:
            raise ValueError(
                f"El valor de 'gender' debe ser 'Male' o 'Female'.")
        elif key == "work_type" and person_data[key] not in ["Private",
                                                             "Self-employed",
                                                             "Govt_job",
                                                             "children",
                                                             "Never_worked"]:
            raise ValueError(
                f"El valor de 'work_type' debe ser uno de: 'Private',"
                f"'Self-employed', 'Govt_job', 'children', 'Never_worked'.")
        elif key == "Residence_type" and person_data[key] not in ["Urban",
                                                                  "Rural"]:
            raise ValueError(
                f"El valor de 'Residence_type' debe ser 'Urban' o 'Rural'.")
        elif key == "smoking_status" and person_data[key] not in [
                "never smoked", "formerly smoked", "smokes", "Unknown"]:
            raise ValueError(
                f"El valor de 'smoking_status' debe ser uno de:"
                f"'never smoked', 'formerly smoked', 'smokes', 'Unknown'.")

    # Validación de variables booleanas
    for key in ["hypertension", "heart_disease", "ever_married"]:
        if not isinstance(person_data[key], bool):
            raise ValueError(f"El valor de '{key}' debe ser True o False.")

    # Validación de variables numéricas
    for key in NUMERICAL_FEATURES:
        if not isinstance(person_data[key], (int, float)) or person_data[
                key] <= 0:
            raise ValueError(
                f"El valor de '{key}' debe ser un número positivo.")


def get_stroke_prediction(person_data):
    """
    Predice la probabilidad de ictus para un paciente.

    Args:
        person_data (dict): Datos del paciente.

    Returns:
        dict: Probabilidad de ictus y un mensaje explicativo.
    """
    try:
        # Validar entrada
        validate_input(person_data)

        # Preprocesar los datos
        df = pd.DataFrame([person_data])[NUMERICAL_FEATURES +
                                         CATEGORICAL_FEATURES]
        transformed_data = PREPROCESSOR.transform(df)

        # Realizar predicción y convertir a float nativo
        probability = float(MODEL.predict(transformed_data)[0][0])

        return {
            "probability": round(probability, 4),
            "message": f"La probabilidad estimada de ictus es del"
                       f"{probability: .2%}."
        }
    except Exception as e:
        return {
            "probability": None,
            "message": f"Error al calcular la predicción: {str(e)}"
        }
