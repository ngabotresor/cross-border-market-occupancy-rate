#!/bin/bash

# Apply migrations
python manage.py makemigrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn server with SSL/TLS
echo "Starting Gunicorn server..."
gunicorn cross_border_market_system.wsgi:application \
    --bind 0.0.0.0:8000 \
    --certfile=/etc/ssl/cbm/cbm.pem \
    --keyfile=/etc/ssl/cbm/cbm.key
