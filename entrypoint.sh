#!/bin/bash

echo "Ожидание запуска PostgreSQL на $DB_HOST:$DB_PORT..."

timeout=30 
# Если PostgreSQL не запускается за 30 секунд,
# выводится сообщение об ошибке, и скрипт завершает работу.

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then 
        echo "Ошибка: PostgreSQL не запустился за ожидаемое время."
        exit 1
    fi
done

echo "Сборка статических файлов..."
if ! python manage.py collectstatic --no-input; then 
    echo "Ошибка: Не удалось собрать статические файлы"
    exit 1
fi 

exec "$@"

