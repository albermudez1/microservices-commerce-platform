# Usamos la imagen oficial de Node.js (versión 22, como en tu README)
FROM node:22-alpine

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de dependencias primero para aprovechar la caché de Docker
COPY package*.json ./

# Instalamos las dependencias
RUN npm install

# Copiamos el resto del código
COPY . .

# Exponemos el puerto de Express
EXPOSE 3000