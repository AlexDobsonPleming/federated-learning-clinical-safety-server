#!/usr/bin/env sh
set -eux

echo "==> wiping old database"
/bin/rm -f /app/db.sqlite3

echo "==> creating fresh sqlite3 file"
/usr/bin/touch /app/db.sqlite3


echo "==> applying migrations"
python manage.py migrate

echo "==> seeding flmodels"
python manage.py seed_flmodels

echo "==> creating uploader"
python manage.py create_uploader uploader1

exec "$@"