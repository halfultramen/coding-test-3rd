FROM python:3.11-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y \
    build-essential gcc libpq-dev git curl \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# copy app code
COPY app /app/app

# create uploads directory
RUN mkdir -p /app/uploads

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
