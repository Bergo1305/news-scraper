#! /usr/bin/env bash

set -e

# It is better to not use these scripts here because this will be called everytime docker restart.
# Better approach could be in docker exec when services are ready (one time only).


python3 manage.py migrate

python3 manage.py createsuperuserwithpassword \
        --username "$ADMIN_USERNAME" \
        --password "$ADMIN_PASSWORD" \
        --email "$ADMIN_EMAIL"\
        --preserve

python manage.py collectstatic --no-input --clear

exec "$@"
