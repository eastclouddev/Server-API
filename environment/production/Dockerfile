FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"
RUN pip3 install requests

COPY ../../lmsc /app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]