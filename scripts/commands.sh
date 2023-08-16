# try to run as /bin/sh on linux
#!/bin/sh

# ends shell terminal if an error occurs
set -e


# wait until db startup
while ! nc -z $SQL_HOST $SQL_PORT; do
  echo "🟡 Waiting for MYSQL Database Startup ($SQL_HOST $SQL_PORT) ..."
  sleep 2
done

echo "✅ MYSQL Database Started Successfully ($SQL_HOST:$SQL_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000