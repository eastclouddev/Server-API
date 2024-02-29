FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /

RUN pip3 install --upgrade pip
RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"
RUN pip3 install requests
RUN pip3 install sqlalchemy
RUN pip3 install pydantic
RUN pip3 install pydantic_settings
RUN pip3 install psycopg2-binary
RUN pip3 install pytest
RUN pip3 install PyMySQL

COPY ../../app /app
ADD environment/develop/envfile /etc

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]
