FROM python:3.11.5

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

# Copy the Django application code
COPY . /app
WORKDIR /app

# Copy the updated entrypoint script
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the SSL/TLS certificates
VOLUME ["/etc/ssl/cbm"]

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
