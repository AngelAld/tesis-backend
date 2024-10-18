FROM python:3.11.4-alpine

WORKDIR /usr/src/django

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY  ./requirements.txt /usr/src/django/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/django/entrypoint.sh

COPY . /usr/src/django/

ENTRYPOINT [ "/usr/src/django/entrypoint.sh" ]