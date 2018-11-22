#!/usr/bin/env bash

git pull
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic