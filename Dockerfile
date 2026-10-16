# 1. Imagen base oficial de Python
FROM python:3.11-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar primero las dependencias para aprovechar la memoria caché de capas de Docker
COPY requirements.txt .

# 4. Instalar las librerías sin guardar archivos de caché de pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código fuente de la aplicación
COPY . .

# 6. Informar que la aplicación expone el puerto 8501 
EXPOSE 8501

# 7. Comando de arranque vinculando el servidor a 0.0.0.0 para acceso externo
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]