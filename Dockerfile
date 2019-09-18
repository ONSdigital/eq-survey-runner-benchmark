FROM python:3.7-slim

RUN apt-get update && apt-get install -y build-essential curl
RUN pip install pipenv

WORKDIR /app

ENTRYPOINT ["./docker-run.sh"]

COPY . /app

RUN pipenv install --deploy --system
