#!/bin/bash

# Collect static files
echo "Migrate from SQLite to PostgreSQL"
python3 manage.py makemigrations --merge --noinput
python3 manage.py migrate

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000