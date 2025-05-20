FROM python:3.12-slim

WORKDIR /benchmark
COPY . /benchmark

# These dependencies are required for the psutil Python package
RUN apt-get update && apt-get install -y gcc python3-dev

# Install the required dependencies via pip
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip install "poetry==2.1.2" \
    && poetry config virtualenvs.create false \
    && poetry install --only main

# Start Locust using LOCUS_OPTS environment variable
ENTRYPOINT ["bash", "./docker_entrypoint.sh"]