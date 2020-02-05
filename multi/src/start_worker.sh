#!/bin/bash
echo "Starting worker.";
celery -A alpha worker -E -n worker_node_$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo -n '') -l info
echo "Worker down.";