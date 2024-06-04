#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

postgres_is_not_ready() {
python << END
import psycopg2
import sys

try:
    psycopg2.connect(
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}"
    )
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)

sys.exit(0)
END
}

until postgres_is_not_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

echo "$PWD"
TEST_PATH="$PWD"
ls "$TEST_PATH"

#python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8011 config.wsgi --capture-output --worker-class gevent --max-requests $GUNICORN_MAX_REQUESTS --max-requests-jitter $GUNICORN_MAX_REQUESTS_JITTER --workers $GUNICORN_WORKERS --timeout $GUNICORN_TIMEOUT --reload
#else
#    gunicorn \
#        --bind 0.0.0.0:8000 config.wsgi \
#        --capture-output \
#        --worker-class gevent \
#        --max-requests $GUNICORN_MAX_REQUESTS \
#        --max-requests-jitter $GUNICORN_MAX_REQUESTS_JITTER \
#        --workers $GUNICORN_WORKERS \
#        --timeout $GUNICORN_TIMEOUT \
#        --reload
#fi
