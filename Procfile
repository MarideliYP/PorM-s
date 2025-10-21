release: python manage.py migrate --noinput
web: gunicorn PrMas.wsgi:application --bind 0.0.0.0:$PORT
