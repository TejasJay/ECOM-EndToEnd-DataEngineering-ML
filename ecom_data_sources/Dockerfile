FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH="/app"

# Install pgrep + Python dependencies
RUN apt-get update && apt-get install -y procps && \
    pip install --upgrade pip && pip install -r requirements.txt

CMD ["bash", "start_simulation.sh"]



