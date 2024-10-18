#!/bin/ash

echo "Applying database migrations..."

python manage.py migrate

echo "Starting server..."

exec "$@" 