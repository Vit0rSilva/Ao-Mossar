FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponha a porta 80 (o padrão da web)
EXPOSE 80

# Rode o Uvicorn na porta 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
