#!/bin/bash
echo "Container booted."
echo "Making Django migrations."
python manage.py makemigrations
echo "Running Django migrations."
python manage.py migrate
echo "Starting Django server."
python manage.py runserver 8000