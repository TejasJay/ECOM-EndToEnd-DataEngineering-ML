FROM python:3.11-slim

WORKDIR /app

# ✅ Optional: install debugging tools
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy all source files
COPY . .

# 🔥 Replace shell script with direct Python command 
CMD ["python3", "-u", "test_consumer.py"]

