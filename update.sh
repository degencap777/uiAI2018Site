#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
cp -rv main/static static/main
cp -rv blog/static static/blog
cp -rv user_panel/static static/user_panel
export UIAI2018_DEBUG=FALSE