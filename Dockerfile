FROM python:3.10-slim

WORKDIR /benchmark
COPY . /benchmark

# These dependencies are required for the psutil Python package
RUN apt-get update && apt-get install -y gcc python3-dev

# Install the required dependencies via pip
RUN pip install pipenv==2022.9.24
RUN pipenv install --deploy --system

# Start Locust using LOCUS_OPTS environment variable
ENTRYPOINT ["bash", "./docker_entrypoint.sh"]