FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e força flush imediato dos prints
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências de compilação mínimas caso necessário
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pasta para persistência do banco SQLite
VOLUME ["/app/data"]

CMD ["python", "bot.py"]
