#!/bin/sh
echo "Container booted."
echo "Waiting for 10 seconds to allow postgres to boot."
sleep 10
echo "Making Django migrations."
python manage.py makemigrations
echo "Running Django migrations."
python manage.py migrate
echo "Starting Django server."
python manage.py runserver 8000
