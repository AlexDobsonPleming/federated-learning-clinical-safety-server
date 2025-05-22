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

# if we’re in “demo” mode, create the demo superuser
if [ -n "$DEMO_USERNAME" ] && [ -n "$DEMO_PASSWORD" ]; then
  echo "==> ensuring demo user exists"
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$DEMO_USERNAME").exists():
    User.objects.create_superuser(
        username="$DEMO_USERNAME",
        email="${DEMO_EMAIL:-demo@example.com}",
        password="$DEMO_PASSWORD"
    )
EOF
fi

exec "$@"