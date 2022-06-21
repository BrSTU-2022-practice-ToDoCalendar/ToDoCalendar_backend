FROM python:3.10.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN apt-get update && apt-get -y install gcc gettext

RUN pip install pipenv \
    && pipenv install --deploy --system --ignore-pipfile

#COPY entrypoint.sh /app/
#RUN chmod +x entrypoint.sh

COPY . /app/
