#!/usr/bin/env bash

git pull
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
sudo service uwsgi restart
sudo service nginx restart