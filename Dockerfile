FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpcre2-8-0 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --upgrade setuptools

COPY ./app /code/app

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]