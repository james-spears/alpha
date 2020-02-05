#!/bin/sh

/etc/init.d/celeryd start

until /etc/init.d/celeryd status; do
  sleep 2
  echo "Retry!";
done

echo "Celery worker daemon is ready.";

/etc/init.d/celerybeat start

until /etc/init.d/celerybeat status; do
  sleep 2
  echo "Retry!";
done

echo "Celery beat daemon is ready.";

su - docker

python3 manage.py makemigrations
until python3 manage.py migrate; do
  sleep 2
  echo "Retry migrations.";
done

echo "Migrations successful.";

python3 manage.py create_superuser --username=$ADMIN_USERNAME --email=$ADMIN_EMAIL --password=$ADMIN_PASSWORD

sleep 5
echo "Django is ready.";

gunicorn $DJANGO_APP_MODULE.wsgi \
  --workers=3 \
  --worker-class=eventlet\
  --timeout=30 \
  --bind=0.0.0.0:8000 \
  --user=$GUNICORN_USER \
  --group=$GUNICORN_GROUP