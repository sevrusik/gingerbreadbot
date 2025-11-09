#!/bin/bash

# Скрипт запуска gingerbread-bot

set -e

echo "🍪 Запуск бота для заказа пряников..."

# Переходим в директорию проекта
cd "$(dirname "$0")/.."

# Проверяем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "Запустите сначала: ./scripts/setup.sh"
    exit 1
fi

# Активируем виртуальное окружение
echo "🔌 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем .env файл
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте .env файл с настройками"
    exit 1
fi

# Проверяем что токен бота указан
if grep -q "your_bot_token_here" .env; then
    echo "❌ Токен бота не настроен!"
    echo "Отредактируйте .env файл и укажите TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Создаем директории если их нет
mkdir -p logs database backups

# Создаем лог файл
LOG_FILE="logs/bot_$(date +%Y%m%d_%H%M%S).log"

echo "📝 Лог файл: $LOG_FILE"
echo "🚀 Запуск бота..."
echo ""

# Запускаем бота с логированием
python run.py 2>&1 | tee "$LOG_FILE"