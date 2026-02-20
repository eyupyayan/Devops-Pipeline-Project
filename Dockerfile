FROM python:3.11-slim

WORKDIR /app

# Kopier og installer dependencies først (bedre caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopier app-koden
COPY app ./app

EXPOSE 8000

# Kjør API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
