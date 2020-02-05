#!/bin/bash
echo "Starting monitor.";
if [ $LOCAL -eq 1 ]; then
    echo "Starting monitor for local env.";
    # # on local use the below line
    celery flower -A alpha \
    --basic_auth=$ADMIN_USERNAME:$ADMIN_PASSWORD \
    --broker=$CELERY_BROKER_URL \
    --broker_api=$CELERY_BROKER_URL \
    --inspect_timeout=10000 \
    --address=0.0.0.0 \
    --port=5555
else
    echo "Starting monitor for remote env.";
    # on server use the below line
    celery flower -A alpha \
    --basic_auth=$ADMIN_USERNAME:$ADMIN_PASSWORD \
    --broker=$CELERY_BROKER_URL \
    --broker_api=$CELERY_BROKER_URL \
    --inspect_timeout=10000 \
    --address=0.0.0.0 \
    --port=5555 \
    --url_prefix=flower
fi
echo "Monitor down.";