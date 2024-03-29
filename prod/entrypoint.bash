#!/bin/bash
cd /venueless/server || exit
export DJANGO_SETTINGS_MODULE=venueless.settings
export VENUELESS_DATA_DIR=/data/
export HOME=/venueless
export NUM_WORKERS=${VENUELESS_WORKERS:-$((2 * $(nproc --all)))}

if [ ! -d /data/logs ]; then
    mkdir /data/logs;
fi
if [ ! -d /data/media ]; then
    mkdir /data/media;
fi

if [ "$1" == "all" ]; then
    python3 manage.py migrate --noinput
    exec sudo -E /usr/bin/supervisord -n -c /etc/supervisord.conf
fi

if [ "$1" == "celery" ]; then
    exec celery -A venueless.celery_app worker -l info
fi

if [ "$1" == "webworker" ]; then
    mkdir -p /tmp/venueless
    exec gunicorn -k uvicorn.workers.UvicornWorker --bind unix:/tmp/venueless/websocket.sock -w "$NUM_WORKERS" venueless.asgi:application
fi

if [ "$1" == "shell" ]; then
    exec python3 manage.py shell_plus
fi

exec python3 manage.py "$@"