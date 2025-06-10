FROM python:3.11-slim

# Set working directory early.
WORKDIR /app

# ✅ Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# ✅ Install system packages and Python dependencies (cached if requirements.txt unchanged )
RUN apt-get update && apt-get install -y --no-install-recommends procps \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ✅ Then copy the rest of the source code
COPY . .

# ✅ Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ✅ Run the simulator
CMD ["python3", "-u", "pos_logs/unified_simulator.py"]
