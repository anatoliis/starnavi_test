#!/bin/sh
set -ex

python manage.py makemigrations --check
python manage.py migrate
python manage.py collectstatic --noinput

if [ "$DEBUG" = "True" ]; then
    python manage.py check
else
    python manage.py check  --deploy
fi

uwsgi --ini /opt/sn_api/uwsgi.ini
