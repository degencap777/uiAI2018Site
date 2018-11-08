#!/usr/bin/env bash

git pull
workon uiai2018
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
export UIAI2018_DEBUG=FALSE