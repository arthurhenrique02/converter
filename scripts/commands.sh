#!/bin/sh

# ends shell terminal if an error occurs
set -e

echo "✅ MYSQL Database Started Successfully ($SQL_HOST:$SQL_PORT)"

# Executa as migrações do Django
echo "🟢 Running Django Migrations..."

# make authdb migrations
/venv/bin/python manage.py makemigrations --noinput

# migrate django default apps to mysql db
/venv/bin/python manage.py migrate admin auth contenttypes sessions messages staticfiles --database=auth_db --noinput

# migrate created apps
/venv/bin/python manage.py migrate auth_credentials --database=auth_db --noinput
# mongodb database
/venv/bin/python manage.py migrate --database=files_db --noinput

# Inicia o servidor Django
echo "🟢 Starting Django Server..."
/venv/bin/python manage.py runserver 0.0.0.0:8000