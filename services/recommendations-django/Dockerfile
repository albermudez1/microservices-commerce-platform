# Usamos la imagen oficial de Python 3.13 (versión ligera)
FROM python:3.13-slim

# Instalamos dependencias del sistema requeridas para compilar el conector de PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos SOLO el requirements.txt primero para aprovechar la caché
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del microservicio
COPY . .

# Exponemos el puerto de Django
EXPOSE 8001