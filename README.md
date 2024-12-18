# Task Scheduler

Task Scheduler is a lightweight service designed to manage and execute scheduled tasks that trigger webhooks to specified URLs. It enables users to set up tasks that call designated web URLs at predefined times, making it ideal for automating time-sensitive or recurring operations.

## Technologies Used
  - `Django`: Backend framework for managing tasks and APIs.
  - `MySQL`: Database for storing task metadata.
  - `Celery`: Distributed task queue for scheduling and executing tasks.
  - `RabbitMQ`: Message broker for Celery, enables task persistence in case of failure.

## Prerequisites
  - `Python 3.13` (recommended way of installation is through `pyenv`, refer to the [pyenv installation](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) page)
  - `docker` (refer to the [docker engine installation](https://docs.docker.com/engine/install/) page)
  - `docker-compose` (refer to the [docker compose installation](https://docs.docker.com/compose/install/) page)
  - `direnv` (automatic environment setup tool, refer to the [direnv installation](https://direnv.net/docs/installation.html) page)
    _**Note**: Don't forget to add the following block to the ~/.bashrc file:_
    ```bash
    if command -v -- direnv > /dev/null 2>&1; then
    eval "$(direnv hook bash)"
    fi
    ```
  - `pipenv` (python dependency and virtualenv management tool, install by running `python -m pip install pipenv`)
    _**Note**: Direnv automatically creates a virtual environment in the repository and installs the required Python dependencies, provided it has been correctly configured._

## Getting started

> _**Note**_: Make sure you are in the project root directory

1.  Allow direnv to load environment variables and create python virtual environment with required python dependencies:
    ```sh
    direnv allow
    ```

2.  Start the services:
    _**Note**: This step will automatically build the Docker image for the Django app using the ./Dockerfile and start the necessary side services!_
    ```sh
    docker-compose up -d
    ```

3.  Check the status of the services to ensure they are up and running:
    ```sh
    docker-compose ps
    ```

4.  Access the web app at `http://localhost:8000`.


#### Running Automated Tests

A total of 9 tests have been implemented. To run them, use the following command:
```sh
docker-compose exec -it web python manage.py test
```
