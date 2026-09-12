FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system honeywatch && adduser --system --ingroup honeywatch honeywatch

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY simulation ./simulation
COPY tests ./tests

RUN mkdir -p /app/data /app/logs && chown -R honeywatch:honeywatch /app

USER honeywatch

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
