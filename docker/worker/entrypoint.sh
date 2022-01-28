#! /usr/bin/env bash

set -e

# It is better to not use these scripts here because this will be called everytime docker restart.
# Better approach could be in docker exec when services are ready (one time only).

wait-for-it redis.svc.cluster.local:6379

exec "$@"
