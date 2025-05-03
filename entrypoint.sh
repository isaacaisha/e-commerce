#!/bin/sh

# Exit on error
set -e

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Run the server
exec "$@"
