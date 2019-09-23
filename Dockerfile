FROM python:3.7

WORKDIR /benchmark
COPY . /benchmark

# Install the required dependencies via pip
RUN pip install pipenv==2018.11.26
RUN pipenv install --deploy --system

# Expose the required Locust ports
EXPOSE 5557 5558 8089

# Set script to be executable
RUN chmod 755 run_distributed.sh

# Start Locust using LOCUS_OPTS environment variable
ENTRYPOINT ["bash", "./run_distributed.sh"]