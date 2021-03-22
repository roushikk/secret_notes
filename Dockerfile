FROM python:3.8-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt /
RUN pip install -r /requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
