FROM python:3.11-slim

WORKDIR /app

# Optional: install debugging tools
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start_consumer.sh

CMD ["./start_consumer.sh"]
