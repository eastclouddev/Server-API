FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app .

CMD bash -c "cd /app/database && \
    alembic upgrade head && \
    cd /app && \
    python seed.py && \
    uvicorn main:app --reload --host 0.0.0.0 --port 8080 --log-config core/log_config.yaml"
