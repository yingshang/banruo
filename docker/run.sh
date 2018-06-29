service mysql start
redis-server &
python3 /opt/banruo/manage.py celery -A banruo worker -l info --beat &
python3 /opt/banruo/manage.py runserver 0.0.0.0:8000
