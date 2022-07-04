FROM python:3.10.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv \
    && pipenv install --deploy --system --ignore-pipfile

COPY . /app/

CMD python manage.py migrate && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@mail.ru', 'admin')" && python manage.py runserver 0.0.0.0:8000