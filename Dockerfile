FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY main.py embedded_assets.py /app/

# Les dossiers absents de GitHub mobile sont recréés par embedded_assets.py.
RUN mkdir -p /app/data/uploads

EXPOSE 8000
CMD ["sh", "-c", "mkdir -p /app/data/uploads && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
