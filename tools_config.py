tools = [
    {
        "name": "get_stroke_prediction",
        "description": "Predice la probabilidad de ictus para un paciente.",
        "parameters": {
            "type": "object",
            "required": ["person_data"],
            "properties": {
                "person_data": {
                    "type": "object",
                    "description": "Datos del paciente.",
                    "properties": {
                        "gender": {
                            "type": "string",
                            "description": "Género del paciente, debe ser 'Male' o 'Female'.",
                            "enum": ["Male", "Female"]
                        },
                        "age": {
                            "type": "number",
                            "description": "Edad del paciente en años."
                        },
                        "hypertension": {
                            "type": "boolean",
                            "description": "Indica si el paciente tiene hipertensión."
                        },
                        "heart_disease": {
                            "type": "boolean",
                            "description": "Indica si el paciente tiene enfermedades cardíacas."
                        },
                        "ever_married": {
                            "type": "boolean",
                            "description": "Indica si el paciente ha estado alguna vez casado."
                        },
                        "work_type": {
                            "type": "string",
                            "description": "Tipo de trabajo del paciente.",
                            "enum": ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]
                        },
                        "Residence_type": {
                            "type": "string",
                            "description": "Tipo de residencia del paciente.",
                            "enum": ["Urban", "Rural"]
                        },
                        "avg_glucose_level": {
                            "type": "number",
                            "description": "Nivel promedio de glucosa en sangre."
                        },
                        "bmi": {
                            "type": "number",
                            "description": "Índice de masa corporal del paciente."
                        },
                        "smoking_status": {
                            "type": "string",
                            "description": "Estado de tabaquismo del paciente.",
                            "enum": ["never smoked", "formerly smoked", "smokes", "Unknown"]
                        }
                    },
                    "required": [
                        "gender",
                        "age",
                        "hypertension",
                        "heart_disease",
                        "ever_married",
                        "work_type",
                        "Residence_type",
                        "avg_glucose_level",
                        "bmi",
                        "smoking_status"
                    ],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "validate_input",
        "description": "Validates that the input data contains all necessary keys and checks their values.",
        "parameters": {
            "type": "object",
            "required": ["person_data"],
            "properties": {
                "person_data": {
                    "type": "object",
                    "description": "Información de la persona que necesita validarse.",
                    "properties": {
                        "gender": {
                            "type": "string",
                            "description": "Género de la persona; debe ser 'Male' o 'Female'.",
                            "enum": ["Male", "Female"]
                        },
                        "work_type": {
                            "type": "string",
                            "description": "Tipo de trabajo; debe ser una de las categorías predefinidas.",
                            "enum": ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]
                        },
                        "Residence_type": {
                            "type": "string",
                            "description": "Tipo de residencia; debe ser 'Urban' o 'Rural'.",
                            "enum": ["Urban", "Rural"]
                        },
                        "smoking_status": {
                            "type": "string",
                            "description": "Estado de tabaquismo; debe ser una de las categorías predefinidas.",
                            "enum": ["never smoked", "formerly smoked", "smokes", "Unknown"]
                        },
                        "hypertension": {
                            "type": "boolean",
                            "description": "Indica si la persona tiene hipertensión; debe ser True o False."
                        },
                        "heart_disease": {
                            "type": "boolean",
                            "description": "Indica si la persona tiene enfermedad cardíaca; debe ser True o False."
                        },
                        "ever_married": {
                            "type": "boolean",
                            "description": "Indica si la persona ha estado alguna vez casada; debe ser True o False."
                        }
                    },
                    "required": [
                        "gender",
                        "work_type",
                        "Residence_type",
                        "smoking_status",
                        "hypertension",
                        "heart_disease",
                        "ever_married"
                    ],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_reverted_shap_explanation",
        "description": "Combina la generación de valores SHAP y la reversión de los datos transformados. Devuelve un objeto shap.Explanation cuyas 'data' y 'feature_names' coinciden con los valores originales en lugar de los datos escalados/one-hot.",
        "parameters": {
            "type": "object",
            "required": ["person_data"],
            "properties": {
                "person_data": {
                    "type": "object",
                    "description": "Diccionario con los datos de una persona",
                    "properties": {
                        "age": {
                            "type": "number",
                            "description": "Edad de la persona"
                        },
                        "avg_glucose_level": {
                            "type": "number",
                            "description": "Nivel promedio de glucosa"
                        },
                        "bmi": {
                            "type": "number",
                            "description": "Índice de masa corporal"
                        },
                        "gender": {
                            "type": "string",
                            "description": "Género de la persona"
                        },
                        "hypertension": {
                            "type": "boolean",
                            "description": "Si la persona tiene hipertensión o no"
                        },
                        "heart_disease": {
                            "type": "boolean",
                            "description": "Si la persona tiene enfermedad cardíaca o no"
                        },
                        "ever_married": {
                            "type": "boolean",
                            "description": "Si la persona se ha casado alguna vez"
                        },
                        "work_type": {
                            "type": "string",
                            "description": "Tipo de trabajo de la persona"
                        },
                        "Residence_type": {
                            "type": "string",
                            "description": "Tipo de residencia de la persona"
                        },
                        "smoking_status": {
                            "type": "string",
                            "description": "Estado de fumar de la persona"
                        }
                    },
                    "required": [
                        "age",
                        "avg_glucose_level",
                        "bmi",
                        "gender",
                        "hypertension",
                        "heart_disease",
                        "ever_married",
                        "work_type",
                        "Residence_type",
                        "smoking_status"
                    ],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_force_plot",
        "description": "Generates a force plot using SHAP values and returns the figure.",
        "parameters": {
            "type": "object",
            "required": ["shap_explanation"],
            "properties": {
                "shap_explanation": {
                    "type": "object",
                    "description": "SHAP explanation object containing base_values, values, and feature_names.",
                    "properties": {
                        "base_values": {
                            "type": "array",
                            "description": "An array of base values used in SHAP calculations.",
                            "items": {
                                "type": "number",
                                "description": "Base value for the respective feature."
                            }
                        },
                        "values": {
                            "type": "array",
                            "description": "An array of SHAP values for features.",
                            "items": {
                                "type": "number",
                                "description": "SHAP value for the respective feature."
                            }
                        },
                        "feature_names": {
                            "type": "array",
                            "description": "An array of feature names corresponding to the SHAP values.",
                            "items": {
                                "type": "string",
                                "description": "Name of the feature."
                            }
                        }
                    },
                    "required": [
                        "base_values",
                        "values",
                        "feature_names"
                    ],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_waterfall_plot",
        "description": "Genera un SHAP waterfall plot con un máximo de 'max_display' features y devuelve el objeto figura de matplotlib.",
        "parameters": {
            "type": "object",
            "properties": {
                "shap_explanation": {
                    "type": "object",
                    "description": "Objeto shap_explanation (lista o array de SHAP values) para graficar."
                },
                "max_display": {
                    "type": "integer",
                    "description": "Número máximo de características a mostrar en el plot. Por defecto, 10."
                }
            },
            "required": ["shap_explanation"]
        }
    },
    {
        "name": "get_decision_plot",
        "description": "Genera un decision plot de SHAP para un índice específico.",
        "parameters": {
            "type": "object",
            "required": ["shap_explanation"],
            "properties": {
                "shap_explanation": {
                    "type": "object",
                    "description": "Objeto SHAP que contiene la explicación del modelo.",
                    "properties": {
                        "base_values": {
                            "type": "array",
                            "description": "Valores base para la predicción.",
                            "items": {
                                "type": "number",
                                "description": "Valor base para un caso específico."
                            }
                        },
                        "values": {
                            "type": "array",
                            "description": "Valores SHAP para el caso específico.",
                            "items": {
                                "type": "number",
                                "description": "Valor SHAP para un caso específico."
                            }
                        },
                        "feature_names": {
                            "type": "array",
                            "description": "Nombres de las características utilizadas en el modelo.",
                            "items": {
                                "type": "string",
                                "description": "Nombre de una característica del modelo."
                            }
                        }
                    },
                    "required": [
                        "base_values",
                        "values",
                        "feature_names"
                    ],
                    "additionalProperties": False
                }
            },
            "additionalProperties": False
        }
    }
]
