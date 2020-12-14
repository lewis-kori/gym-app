#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files
touch /gunicorn/logs/access.log
touch /gunicorn/logs/error.log

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn gym.wsgi:application \
    --bind 0.0.0.0:8070 \
    --workers 3 \
    --timeout 180 \
    --log-level=info \
    --access-logfile=/gunicorn/logs/access.log \
    --error-logfile=/gunicorn/logs/error.log \
    --capture-output \
    "$@"
