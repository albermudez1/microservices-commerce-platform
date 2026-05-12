# Usamos la imagen oficial de Python 3.13 (versión ligera)
FROM python:3.13-slim

# Instalamos dependencias del sistema operativo que suelen requerir las librerías de MySQL en Python
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos primero SOLO el requirements.txt
# Esto es un truco de Docker para aprovechar la caché y no reinstalar todo si solo cambiaste tu código
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto del código del microservicio
COPY . .

# Exponemos el puerto de Flask
EXPOSE 5001