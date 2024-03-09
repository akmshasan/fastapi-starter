FROM python:3.11.8-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./api
COPY ./fruits.db ./fruits.db

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
