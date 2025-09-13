FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y build-essential gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar código
COPY src /app

# Variables de entorno
ENV PORT=8080
EXPOSE 8080

# Iniciar con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT}", "main:app"]
