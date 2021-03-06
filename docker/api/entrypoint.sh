#! /usr/bin/env bash

set -e

# It is better to not use these scripts here because this will be called everytime docker restart.
# Better approach could be in docker exec when services are ready (one time only).

wait-for-it postgres.svc.cluster.local:5432

python3 manage.py migrate

python3 manage.py createsuperuserwithpassword \
        --username "$ADMIN_USERNAME" \
        --password "$ADMIN_PASSWORD" \
        --email "$ADMIN_EMAIL"\
        --preserve

python manage.py collectstatic --no-input --clear

python manage.py test

exec "$@"
