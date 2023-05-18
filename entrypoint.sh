#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi
  python3 manage.py migrate
  python3 manage.py collectstatic --no-input
  python3 manage.py init_users
  python3 manage.py init_fruits
  python3 manage.py init_bank
  python3 manage.py start_tasks
exec "$@"