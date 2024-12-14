# syntax=docker/dockerfile:1
FROM python:3.13.1-slim

ARG ENVIRONMENT
ARG APP_PATH="/task_scheduler"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY task_scheduler ${APP_PATH}/task_scheduler
COPY manage.py ${APP_PATH}/
COPY Pipfile ${APP_PATH}/
COPY Pipfile.lock ${APP_PATH}/
COPY pyproject.toml ${APP_PATH}/

WORKDIR /task_scheduler

ENV PYTHONPATH=${APP_PATH}

RUN [ "${ENVIRONMENT}" == "dev" ] && pipenv install --dev || pipenv install

CMD pipenv run python manage.py runserver 0.0.0.0:8000
