FROM python:3.11-slim

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the topic script
COPY create_topics.py .

# Run the topic creation script
CMD ["python3", "create_topics.py"]

