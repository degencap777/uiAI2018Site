#!/usr/bin/env bash

git pull
pip install -r requirements
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic