# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the data processor script
COPY data_processor.py .

# Set environment variables (optional, can also be set in docker-compose.yml)
ENV KAFKA_BOOTSTRAP_SERVERS=broker:9092

# Run the data processor script
CMD ["python", "data_processor.py"]