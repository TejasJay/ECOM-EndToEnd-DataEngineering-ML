FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

RUN apt-get update && apt-get install -y procps && \
    pip install --upgrade pip && pip install -r requirements.txt

CMD ["python3", "-u", "pos_logs/unified_simulator.py"]
