#!/bin/bash

set -e
cd /app

# Wait for Postgres to get ready.
until echo '\q' | ./manage.py dbshell &> /dev/null; do
    sleep 1
done

python manage.py collectstatic --clear --link --no-input