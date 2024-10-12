# Build final image
FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app

# Update base image
RUN apt-get update && \
    apt-get full-upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN mkdir -p /app/data
