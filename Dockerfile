FROM python:3.10.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY . /app/

RUN pip install pipenv \
    && pipenv install --deploy --system --ignore-pipfile
