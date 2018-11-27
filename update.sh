#!/usr/bin/env bash

echo "PULLING FROM GIT..."
git pull
echo "INSTALLING REQUIREMENTS..."
pip install -r requirements.txt
echo "RUNNING DJANGO MIGRATIONS..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
echo "RESTARTING SERVICES..."
sudo service uwsgi restart
sudo service nginx restart