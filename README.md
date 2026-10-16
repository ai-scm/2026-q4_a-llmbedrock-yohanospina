# Asistente AWS Bedrock (RAG y LLMs)

Asistente conversacional especializado en la preparación para la certificación AWS Certified AI Practitioner, enfocado en Inteligencia Artificial Generativa, Large Language Models (LLMs) y Retrieval-Augmented Generation (RAG).

## 1. Descripción del Proyecto

El objetivo de esta aplicación es ofrecer un tutor pedagógico e interactivo para estudiantes y profesionales que se preparan para la certificación AWS Certified AI Practitioner. 

El asistente utiliza Amazon Bedrock Runtime a través de la API Converse para interactuar con modelos fundacionales como Amazon Nova (por ejemplo, `amazon.nova-lite-v1:0`), integrando un prompt de sistema estructurado que guía las respuestas con explicaciones teóricas, casos de uso arquitectónicos y preguntas de comprobación de aprendizaje.

## 2. Tecnologías Utilizadas

- Python 3.11 / 3.12
- Streamlit (Interfaz de usuario web conversacional)
- Amazon Bedrock Runtime (Inferencia de modelos fundacionales mediante boto3 y Converse API)
- Boto3 (SDK oficial de AWS para Python)
- Docker (Contenerización e infraestructura de despliegue local)
- python-dotenv (Gestión de variables de entorno)
- Git y GitHub (Control de versiones)

## 3. Estructura del Repositorio

```text
asistente-bedrock-rag/
│
├── .env.example          # Plantilla de variables de entorno (sin credenciales)
├── .dockerignore         # Filtro de archivos excluidos en la construcción de la imagen Docker
├── .gitignore            # Exclusión de credenciales y entornos virtuales en Git
├── Dockerfile            # Receta de construcción del contenedor Docker
├── README.md             # Documentación del proyecto
├── app.py                # Aplicación principal de Streamlit y conexión con Bedrock
├── requirements.txt      # Dependencias del proyecto en Python
├── system_prompt.py      # Instrucciones y perfil experto del asistente
└── test_bedrock.py       # Script de prueba y diagnóstico de conexión con AWS Bedrock
```

## 4. Requisitos Previos

1. Tener instalado Python 3.11 o superior.
2. Tener instalado Docker en tu sistema local.
3. Contar con una cuenta de AWS con acceso habilitado a Amazon Bedrock en la región `us-east-1` (o la región configurada).
4. Obtener las credenciales temporales de AWS (AWS Access Key ID, AWS Secret Access Key y AWS Session Token).

## 5. Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto basado en la plantilla `.env.example`:

```ini
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
AWS_SESSION_TOKEN=tu_session_token
AWS_DEFAULT_REGION=us-east-1
MODEL_ID=amazon.nova-lite-v1:0
```

Importante: El archivo `.env` contiene credenciales sensibles y está excluido mediante `.gitignore` para prevenir cualquier filtración en repositorios públicos o compartidos.

## 6. Ejecución Local con Python

### Paso 1: Crear y activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate   # En Linux/macOS
# En Windows: venv\Scripts\activate
```

### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Probar la conexión con Bedrock
```bash
python test_bedrock.py
```

### Paso 4: Iniciar la interfaz web
```bash
streamlit run app.py
```
Navega a http://localhost:8501 en tu navegador web.

## 7. Ejecución con Docker

### Paso 1: Limpiar saltos de línea invisibles en el archivo .env (Linux/WSL)
```bash
sed -i 's/\r$//' .env
```

### Paso 2: Construir la imagen de Docker
```bash
docker build -t asistente-bedrock-rag .
```

### Paso 3: Iniciar el contenedor
```bash
docker run -p 8501:8501 --env-file .env asistente-bedrock-rag
```

Accede a la aplicación en http://localhost:8501.

## 8. Seguridad y Buenas Prácticas

- Las credenciales de AWS no forman parte de las capas de la imagen Docker gracias al archivo `.dockerignore`.
- El archivo `.env` jamás debe subirse al control de versiones (protegido en `.gitignore`).
- La memoria de conversación se gestiona en tiempo de ejecución mediante `st.session_state` de Streamlit.
