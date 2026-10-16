import os
import boto3
import streamlit as st
from dotenv import load_dotenv
from system_prompt import SYSTEM_PROMPT

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración visual de la ventana del navegador
st.set_page_config(
    page_title="Asistente RAG & LLMs - AWS Bedrock",
    page_icon="🗿",
    layout="centered",
)

st.title("Asistente AWS Bedrock (RAG & LLMs)")
st.caption("Especializado en la certificación AWS Certified AI Practitioner")


# 2. Inicializar el cliente de Bedrock Runtime (con caché de recursos)
@st.cache_resource
def obtener_cliente_bedrock():
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region)


try:
    bedrock_client = obtener_cliente_bedrock()
except Exception as e:
    st.error(f"Error al inicializar el cliente de AWS: {e}")
    st.stop()

model_id = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")

# 3. Inicializar el historial de conversación en st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Renderizar todo el historial de chat acumulado en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Extraer el texto dentro del formato de la API Converse
        texto = (
            message["content"][0]["text"]
            if isinstance(message["content"], list)
            else message["content"]
        )
        st.markdown(texto)

# 5. Capturar la entrada de texto del usuario
if prompt := st.chat_input("Hazme una pregunta sobre RAG, LLMs o Bedrock..."):
    # Guardar y mostrar el mensaje del usuario
    user_msg = {"role": "user", "content": [{"text": prompt}]}
    st.session_state.messages.append(user_msg)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar la respuesta del asistente usando la API Converse
    with st.chat_message("assistant"):
        with st.spinner("Consultando a Amazon Bedrock..."):
            try:
                # Enviamos el historial completo acumulado para mantener el contexto
                response = bedrock_client.converse(
                    modelId=model_id,
                    messages=st.session_state.messages,
                    system=[{"text": SYSTEM_PROMPT}],
                    inferenceConfig={"temperature": 0.7, "maxTokens": 1000},
                )

                # Extraer la respuesta textual devuelta por el modelo
                response_text = response["output"]["message"]["content"][0][
                    "text"
                ]
                st.markdown(response_text)

                # Guardar la respuesta del asistente en el historial de sesión
                assistant_msg = {
                    "role": "assistant",
                    "content": [{"text": response_text}],
                }
                st.session_state.messages.append(assistant_msg)

            except Exception as e:
                error_msg = str(e)
                if (
                    "ExpiredToken" in error_msg
                    or "UnrecognizedClientException" in error_msg
                ):
                    st.error(
                        "Tu token de sesión de AWS ha expirado. Actualiza las credenciales en `.env` y reinicia la app."
                    )
                else:
                    st.error(f"Error al comunicarse con Bedrock: {error_msg}")