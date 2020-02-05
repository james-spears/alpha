#!/bin/bash
python3 manage.py makemigrations
until python3 manage.py migrate; do
  sleep 2
  echo "Retry migrations.";
done

echo "Migrations successful.";

python3 manage.py create_superuser --username=$ADMIN_USERNAME --email=$ADMIN_EMAIL --password=$ADMIN_PASSWORD
sleep 5
echo "Django is ready.";
echo "Starting WSGI server.";
whoami;
echo "gunicorn user: "$GUNICORN_USER;
echo "gunicorn group: "$GUNICORN_GROUP;
gunicorn $DJANGO_APP_MODULE.wsgi \
  --workers=3 \
  --worker-class=eventlet\
  --timeout=30 \
  --bind=0.0.0.0:8000 \
  --user=$GUNICORN_USER \
  --group=$GUNICORN_GROUP
echo "WSGI server down.";
