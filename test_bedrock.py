import os
import boto3
from dotenv import load_dotenv
from system_prompt import SYSTEM_PROMPT

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()


def probar_conexion_bedrock():
    # 2. Extraer configuraciones de entorno
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    model_id = os.getenv(
        "MODEL_ID", "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    )

    print(f"Intentando conectar a Bedrock en la región: {region}...")
    print(f"Usando el modelo: {model_id}\n")

    try:
        # 3. Inicializar el cliente Bedrock Runtime con boto3
        # Boto3 detecta automáticamente las variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY y AWS_SESSION_TOKEN
        client = boto3.client("bedrock-runtime", region_name=region)

        # 4. Construir la estructura del mensaje para la API Converse
        mensajes_prueba = [
            {
                "role": "user",
                "content": [
                    {"text": "¿Qué es RAG y por qué es importante para un LLM?"}
                ],
            }
        ]

        # 5. Ejecutar la llamada mediante la API Converse de Bedrock
        respuesta = client.converse(
            modelId=model_id,
            messages=mensajes_prueba,
            system=[{"text": SYSTEM_PROMPT}],
            inferenceConfig={"temperature": 0.7, "maxTokens": 500},
        )

        # 6. Extraer el texto retornado por el modelo
        texto_respuesta = respuesta["output"]["message"]["content"][0]["text"]

        print("¡Conexión exitosa a Amazon Bedrock!\n")
        print("--- Respuesta del Asistente ---")
        print(texto_respuesta)
        return True

    except Exception as e:
        print("Error al conectar con Amazon Bedrock:")
        print(str(e))
        return False


if __name__ == "__main__":
    probar_conexion_bedrock()