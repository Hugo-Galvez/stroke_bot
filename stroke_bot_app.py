from openai import OpenAI
import streamlit as st
import os
import shelve
import json
import stroke_prediction as sp
import stroke_SHAP as shp
from tools_config import tools

# Definición de herramientas para GPT
tools = tools


# Configuración de la página y variables iniciales
st.set_page_config(page_title="Stroke Bot", layout="wide")
st.title("🩺 Stroke Bot: un asistente médico para predicción de ictus")

USER_AVATAR = "👩‍⚕️"
BOT_AVATAR = "🧠"

client = OpenAI(api_key=st.secrets["API_KEY"])
LLM_MODEL = "gpt-4o-mini-2024-07-18"


def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def create_function_message(name: str, payload: dict) -> dict:
    """
    Crea un mensaje con role='function' para alimentar a GPT
    tras la llamada a una de las funciones.
    """
    return {"role": "function", "name": name, "content": json.dumps(payload)}


app_info = load_text("app_info.txt")
accepted_variables = load_text("accepted_variables.txt")

system_message = {
    "role": "system",
    "content": load_text("system_message.txt")
}

if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns([1.5, 2])

with col1:
    with st.expander("ℹ️ Información sobre la aplicación", expanded=True):
        st.markdown(app_info)
    with st.expander("📋 Variables aceptadas y su descripción"):
        st.markdown(accepted_variables)

with col2:
    st.subheader("💬 Interacción con Stroke Bot")

    # Renderizar mensajes del usuario y del asistente
    for message in st.session_state.messages:
        if message["role"] in ("assistant", "user"):
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu mensaje:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        # Enviar mensajes al modelo GPT luego de recibir el prompt del
        # usuario y guardarlo

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[system_message] + st.session_state.messages,
            functions=tools,
            function_call="auto"
        )

        message = response.choices[0].message

        while True:
            if message.function_call:
                func_call = message.function_call
                arguments = json.loads(func_call.arguments)

                if func_call.name == "get_stroke_prediction":
                    person_data = arguments["person_data"]
                    prediction_result = sp.get_stroke_prediction(person_data)

                    st.session_state.messages.append(
                        create_function_message(func_call.name,
                                                prediction_result)
                    )

                elif func_call.name == "validate_input":
                    person_data = arguments["person_data"]
                    try:
                        sp.validate_input(person_data)
                        validation_result = {"valid": True,
                                             "message": "Datos válidos."}
                    except Exception as e:
                        validation_result = {"valid": False, "message": str(e)}

                    st.session_state.messages.append(
                        create_function_message(func_call.name,
                                                validation_result)
                    )

                elif func_call.name == "get_reverted_shap_explanation":
                    person_data = arguments["person_data"]
                    shap_explanation = shp.get_reverted_shap_explanation(
                        person_data)
                    st.session_state[
                        "reverted_shap_explanation"] = shap_explanation

                    base_values_list = shap_explanation.base_values.tolist()
                    data_list = shap_explanation.data.tolist()
                    values_list = shap_explanation.values.tolist()
                    feature_names = shap_explanation.feature_names

                    response_dict = {
                        "base_values": base_values_list,
                        "data": data_list,
                        "values": values_list,
                        "feature_names": feature_names
                    }

                    st.session_state.messages.append(
                        create_function_message(func_call.name, response_dict)
                    )

                elif func_call.name == "get_force_plot":
                    shap_explanation = st.session_state.get(
                        "reverted_shap_explanation")
                    if shap_explanation is None:
                        function_result = {
                            "error": "No hay 'reverted_shap_explanation' en "
                                     "la sesión."
                                     "Primero genera la explicación."
                        }
                    else:
                        fig = shp.get_force_plot(shap_explanation)
                        st.pyplot(fig)
                        function_result = {
                            "status": "Force plot generado y mostrado en la "
                                      "interfaz."
                        }

                    st.session_state.messages.append(
                        create_function_message(func_call.name,
                                                function_result)
                    )

                elif func_call.name == "get_waterfall_plot":
                    shap_explanation = st.session_state.get(
                        "reverted_shap_explanation")
                    if shap_explanation is None:
                        function_result = {
                            "error": "No hay 'reverted_shap_explanation' en "
                                     "la sesión."
                                     "Primero genera la explicación."
                        }
                    else:
                        max_display = arguments.get("max_display", 10)
                        fig = shp.get_waterfall_plot(shap_explanation,
                                                     max_display=max_display)
                        st.pyplot(fig)
                        function_result = {
                            "status": f"Waterfall plot generado con "
                                      f"max_display={max_display}."
                        }

                    st.session_state.messages.append(
                        create_function_message(func_call.name,
                                                function_result)
                    )

                elif func_call.name == "get_decision_plot":
                    shap_explanation = st.session_state.get(
                        "reverted_shap_explanation")
                    if shap_explanation is None:
                        function_result = {
                            "error": "No hay 'reverted_shap_explanation' en "
                                     "la sesión. Primero genera la "
                                     "explicación."
                        }
                    else:
                        fig = shp.get_decision_plot(shap_explanation)
                        st.pyplot(fig)
                        function_result = {
                            "status": "Decision plot generado y mostrado en "
                                      "la interfaz."
                        }

                    st.session_state.messages.append(
                        create_function_message(func_call.name,
                                                function_result)
                    )

                # Segunda llamada a GPT con el historial
                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[system_message] + st.session_state.messages
                )
                message = response.choices[0].message

            else:
                # Si GPT no llama a ninguna función, da su "respuesta final"
                break

        # Al salir del bucle, 'message' es la resp final (assistant) de GPT
        assistant_reply = message.content
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.markdown(assistant_reply)
