release: python manage.py migrate --no-input
web: gunicorn --bind="${HOST:-0.0.0.0}:${PORT:-5000}" --log-file=- --log-level=INFO --capture-output conf.wsgi:application
worker: python manage.py rqworker