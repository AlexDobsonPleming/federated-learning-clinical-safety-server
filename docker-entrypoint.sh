#!/usr/bin/env sh
set -eux

echo "==> applying migrations"
python manage.py migrate

echo "==> seeding flmodels"
python manage.py seed_flmodels

echo "==> creating uploader"
python manage.py create_uploader uploader1

echo "==> starting server"
exec python manage.py runserver 0.0.0.0:8000 --noreload