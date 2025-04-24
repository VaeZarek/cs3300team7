#!/bin/bash

# Collect static files
echo "Migrate from SQLite to PostgreSQL"
python manage.py makemigrations --merge --noinput
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000