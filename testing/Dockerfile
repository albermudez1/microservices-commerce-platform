# Usamos Python 3.13 slim
FROM python:3.13-slim

# Instalamos dependencias básicas para red
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos el requirements y lo instalamos
# Nota: Ignoramos pywin32 ya que es exclusivo de Windows y fallaría en Linux/Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir locust requests python-dotenv

# Copiamos todo el contenido de la carpeta testing
COPY . .

# Exponemos el puerto de la interfaz web de Locust
EXPOSE 8089

# El comando ejecutará el setup y luego iniciará Locust
CMD ["sh", "-c", "python setup_test_data.py && locust -f locustfile.py --host http://gateway:8000"]