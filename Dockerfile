FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc libffi-dev && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT}", "main:app"]
