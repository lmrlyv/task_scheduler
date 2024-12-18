# syntax=docker/dockerfile:1
FROM python:3.13.1-slim

ARG ENVIRONMENT
ARG ROOT_PATH="/task_scheduler"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1
ENV PYTHONPATH=${ROOT_PATH}
ENV ENVIRONMENT=${ENVIRONMENT}

# Check if ENVIRONMENT is set
RUN [ -n "$ENVIRONMENT" ] || (echo "ERROR: The build-arg 'ENVIRONMENT' is not set!" && exit 1)

RUN apt update; apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN pip install --upgrade pip; pip install pipenv

COPY task_scheduler ${ROOT_PATH}/task_scheduler
COPY pyproject.toml Pipfile Pipfile.lock manage.py ${ROOT_PATH}/

WORKDIR ${ROOT_PATH}

RUN test "${ENVIRONMENT}" = "dev" && pipenv install --dev --system || pipenv install --system

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
