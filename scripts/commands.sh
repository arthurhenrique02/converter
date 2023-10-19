#!/bin/sh

# ends shell terminal if an error occurs
set -e

echo "✅ MYSQL Database Started Successfully ($SQL_HOST:$SQL_PORT)"

# Executa as migrações do Django
echo "🟢 Running Django Migrations..."

# make authdb migrations
/venv/bin/python manage.py makemigrations --noinput
/venv/bin/python manage.py makemigrations converter_service --noinput


# migrate created apps
/venv/bin/python manage.py migrate --database=auth_db --noinput

echo "MYSQL MIGRATIONS DONE"

# mongodb database
/venv/bin/python manage.py migrate --database=videos_db --noinput
/venv/bin/python manage.py migrate --database=mp3s_db --noinput

echo "MONGO MIGRATIONS DONE"

# Inicia o servidor Django
echo "🟢 Starting Django Server..."
/venv/bin/python manage.py runserver 0.0.0.0:8000