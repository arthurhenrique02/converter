#!/bin/sh

# ends shell terminal if an error occurs
set -e

echo "✅ MYSQL Database Started Successfully ($SQL_HOST:$SQL_PORT)"

# Executa as migrações do Django
echo "🟢 Running Django Migrations..."

# make authdb migrations
/venv/bin/python manage.py makemigrations --noinput
/venv/bin/python manage.py migrate --database=auth_db --noinput

# Coleta os arquivos estáticos do Django
echo "🟢 Collecting Django Static Files..."
/venv/bin/python manage.py collectstatic --noinput

# Inicia o servidor Django
echo "🟢 Starting Django Server..."
/venv/bin/python manage.py runserver 0.0.0.0:8000