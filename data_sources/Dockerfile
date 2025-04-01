# Dockerfile to containerize the data_sources simulator

FROM python:3.11-slim

WORKDIR /app

COPY ./data_sources/ .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install -r requirements.txt

ENTRYPOINT ["bash", "./start_simulation.sh"]

