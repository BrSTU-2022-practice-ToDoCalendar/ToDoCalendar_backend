# README

**Языки документации**:

- [English](README.md)
- [Русский](README-ru.md)

**Меню**:

- [Документы](#документы)
- [Стэк приложений](#стэк-приложений)
- [Как запустить приложение для тестирования](#как-запустить-приложение-для-тестирования)
- [Как запустить приложение для разработки](#как-запустить-приложение-для-разработки)
- [Структура проекта](#структура-проекта)

## Документы

- [Задание](https://docs.google.com/document/d/1UQgKfPkB8C36dyDDmPU40rjSw3_fXEH8/edit)
- [Swagger](http://todo-innowise.voilalex.com/swagger/)

## Стэк приложений

- **[Python3.10](https://www.python.org/downloads/release/python-3100/)** - высокоуровневый язык програмирования
- **[Django](https://www.djangoproject.com/)** - веб фреймворк
- **[DRF](https://code.visualstudio.com/#alt-downloads)** - набор инструментов для постороения веб API
- **[pipenv](https://pipenv.pypa.io/en/latest/)** - набор инструментов для создания виртуальной среды и установки пакетов
- **[PyCharm](https://www.jetbrains.com/ru-ru/pycharm/)** - редактор кода
- **[PostgreSQL](https://www.postgresql.org/)** - база данных
- **[Docker](https://www.docker.com/)** - виртуальный контейнер
- **[drf_yasg](https://drf-yasg.readthedocs.io/en/stable/)** - генератор swagger документации
- **[pytest](https://pytest-django.readthedocs.io/en/latest/)** - фреймворк для тестирования
- **[simpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)** - JSON Web Token аутентификация

## Как запустить приложение для тестирования

```bash
git clone https://github.com/ToDoCalendar/ToDoCalendar_backend.git
cd ToDoCalendar_backend
docker-compose up
```

## Как запустить приложение для разработки

```bash
git clone https://github.com/ToDoCalendar/ToDoCalendar_backend.git
cd ToDoCalendar_backend

pip install pipenv
pipenv shell
pipenv install

python manage.py migrate
python manage.py runserver
```

## Структура проекта

```
.
|-- api
|   |-- migrations
|-- tests
|-- ToDoCalendar

4 directories
```