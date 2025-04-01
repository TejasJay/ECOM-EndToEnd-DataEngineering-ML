# Dockerfile to containerize the data_sources simulator

FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Important line: Let Python know where to find `ecom_data_sources`
ENV PYTHONPATH="/app"

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["bash", "start_simulation.sh"]


