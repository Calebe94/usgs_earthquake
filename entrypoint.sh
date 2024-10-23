#!/bin/bash

set -e
export DJANGO_DEBUG=False

echo "$START_TYPE"
if [ "$START_TYPE" = "WEB" ]; then
    echo "Web"
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    uvicorn earthquake_app.asgi:application --host 0.0.0.0 --port 8000
elif [ "$START_TYPE" = "WORKER" ]; then
    echo "Celery"
    celery -A earthquake_app worker --loglevel=INFO
else
    echo "Nothing"
fi
