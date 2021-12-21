#!/bin/sh
echo "Container booted."
echo "Waiting for 30 seconds to allow postgres to boot."
sleep 30
echo "Making Django migrations."
python manage.py makemigrations
echo "Making specific player migrations."
python manage.py makemigrations player
echo "Running Django migrations."
python manage.py migrate
echo "Adding default users from fixture."
python manage.py loaddata seed.json
echo "Starting Django server."
python manage.py runserver 0.0.0.0:8000
