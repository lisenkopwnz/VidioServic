#!/bin/bash

echo "Ожидание запуска PostgreSQL на $DB_HOST:$DB_PORT..."

timeout=60  # Увеличиваем время ожидания до 60 секунд

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
    timeout=$((timeout - 1))

    if [ $timeout -le 0 ]; then
        echo "Ошибка: PostgreSQL не запустился за ожидаемое время."
        exit 1
    fi
done

echo "PostgreSQL доступен. Выполняю сборку статических файлов..."

# Сборка статических файлов
if ! python manage.py collectstatic --no-input; then
    echo "Ошибка: Не удалось собрать статические файлы"
    exit 1
fi

# Запускаем приложение Django
exec "$@"

