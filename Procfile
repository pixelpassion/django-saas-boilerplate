release: python manage.py migrate --no-input
worker: REMAP_SIGTERM=SIGQUIT celery -A conf worker -l INFO --without-heartbeat --without-gossip --without-mingle
web: gunicorn --bind="${HOST:-0.0.0.0}:${PORT:-5000}" --log-file=- --log-level=INFO --capture-output conf.wsgi:application
