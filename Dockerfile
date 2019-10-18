FROM python:3.7-slim

WORKDIR /benchmark
COPY . /benchmark

# Install the required dependencies via pip
RUN pip install pipenv==2018.11.26
RUN pipenv install --deploy --system

# Start Locust using LOCUS_OPTS environment variable
ENTRYPOINT ["bash", "./docker_entrypoint.sh"]