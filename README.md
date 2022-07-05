# README

**Documentation languages**:

- [English](README.md)
- [Русский](README-ru.md)

**Menu**:

- [Documents](#documents)
- [Application stack](#application-stack)
- [How to run app for testing](#how-to-run-app-for-testing)
- [How to run app for development](#how-to-run-app-for-development)
- [Folder structure](#folder-structure)

## Documents

- [Task](https://docs.google.com/document/d/1UQgKfPkB8C36dyDDmPU40rjSw3_fXEH8/edit)
- [Swagger](http://todo-innowise.voilalex.com/swagger/)

## Application stack

- **[Python3.10](https://www.python.org/downloads/release/python-3100/)** - high-level programming language
- **[Django](https://www.djangoproject.com/)** - web framework
- **[DRF](https://code.visualstudio.com/#alt-downloads)** - toolkit for building web APIs
- **[pipenv](https://pipenv.pypa.io/en/latest/)** - toolkit for creation virtual environment and package installation
- **[PyCharm](https://www.jetbrains.com/ru-ru/pycharm/)** - code editor
- **[PostgreSQL](https://www.postgresql.org/)** - database
- **[Docker](https://www.docker.com/)** - virtual container
- **[drf_yasg](https://drf-yasg.readthedocs.io/en/stable/)** - swagger generator
- **[pytest](https://pytest-django.readthedocs.io/en/latest/)** - framework for testing
- **[simpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)** - JSON Web Token authentication

## How to run app for testing

```bash
git clone https://github.com/ToDoCalendar/ToDoCalendar_backend.git
cd ToDoCalendar_backend
docker-compose up
```

## How to run app for development

```bash
git clone https://github.com/ToDoCalendar/ToDoCalendar_backend.git
cd ToDoCalendar_backend

pip install pipenv
pipenv shell
pipenv install

python manage.py migrate
python manage.py runserver
```

## Folder structure

```
.
|-- api
|   |-- migrations
|-- tests
|-- ToDoCalendar

4 directories
```