FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN pip install uv==0.4.29

# Copy dependency files first (layer cache)
COPY apps/api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY apps/api/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
