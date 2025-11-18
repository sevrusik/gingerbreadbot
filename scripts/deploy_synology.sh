#!/bin/bash
# Скрипт для развертывания бота на Synology NAS через docker-compose

set -e  # Остановка при ошибке

echo "🚀 Развертывание Gingerbread Bot на Synology NAS"
echo "================================================"

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте файл .env с переменными окружения:"
    echo ""
    echo "TELEGRAM_BOT_TOKEN=your_token_here"
    echo "ADMIN_USER_IDS=your_user_id"
    echo "DATABASE_URL=postgresql+asyncpg://gingerbread_user:changeme123@postgres:5432/gingerbread_bot"
    echo "POSTGRES_PASSWORD=changeme123"
    exit 1
fi

# Проверка обязательных переменных
source .env
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN не установлен в .env файле!"
    exit 1
fi

if [ -z "$ADMIN_USER_IDS" ]; then
    echo "❌ ADMIN_USER_IDS не установлен в .env файле!"
    exit 1
fi

echo "✅ Файл .env найден и проверен"

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p data/postgres
mkdir -p logs
mkdir -p media/examples

echo "✅ Директории созданы"

# Проверка наличия docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose не найден!"
    echo "Установите docker-compose или используйте 'sudo' для запуска"
    exit 1
fi

# Остановка существующих контейнеров
echo "🛑 Остановка существующих контейнеров..."
docker-compose down 2>/dev/null || true

echo "✅ Контейнеры остановлены"

# Сборка образа
echo "🔨 Сборка Docker образа..."
docker-compose build --no-cache

echo "✅ Образ собран"

# Запуск контейнеров
echo "🚀 Запуск контейнеров..."
docker-compose up -d

echo "✅ Контейнеры запущены"

# Ожидание запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 5

# Проверка статуса
echo "📊 Статус контейнеров:"
docker-compose ps

# Проверка логов
echo ""
echo "📝 Последние логи бота:"
docker-compose logs --tail=20 bot

echo ""
echo "✅ Развертывание завершено!"
echo ""
echo "Полезные команды:"
echo "  docker-compose logs -f bot          # Просмотр логов"
echo "  docker-compose restart bot          # Перезапуск бота"
echo "  docker-compose down                 # Остановка всех сервисов"
echo "  docker-compose up -d --build        # Пересборка и запуск"
