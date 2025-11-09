#!/bin/bash

# Скрипт настройки окружения для gingerbread-bot

set -e

echo "🍪 Настройка окружения для бота заказа пряников..."

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION найден"

# Создаем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔌 Активация виртуального окружения..."
source venv/bin/activate

# Обновляем pip
echo "⬆️ Обновление pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "📥 Установка зависимостей..."
pip install -r requirements.txt

# Создаем необходимые директории
mkdir -p logs backups database

# Проверяем .env файл
if [ ! -f ".env" ]; then
    echo "⚠️ Файл .env не найден"
    echo "Создание шаблона .env..."
    
    cat > .env << EOF
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_USER_ID=your_telegram_user_id

# Database
DATABASE_URL=sqlite:///./database/orders.db

# App Settings
DEBUG=True
LOG_LEVEL=INFO
WEBHOOK_URL=
WEBHOOK_PATH=/webhook
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=8080

# Business Settings
MASTER_NAME=Любовь
BUSINESS_PHONE=+7-xxx-xxx-xx-xx
PICKUP_ADDRESS=ул. Мастеров, 12
PICKUP_COORDINATES=55.7558,37.6176
WORKING_HOURS=10:00-12:00, 18:00-20:00

# Pricing
BASE_PRICE_EUR=2.0
COLORING_PRICE_EUR=3.5
RUSH_ORDER_MULTIPLIER=1.25
MIN_PREPARATION_DAYS=3
EOF

    echo "📝 Создан файл .env с шаблоном настроек"
    echo "⚠️ ВАЖНО: Отредактируйте .env файл с вашими настройками!"
    echo ""
    echo "Необходимо указать:"
    echo "- TELEGRAM_BOT_TOKEN (получите у @BotFather)"
    echo "- ADMIN_USER_ID (ваш Telegram ID)"
    echo "- Остальные настройки бизнеса"
fi

# Проверяем права на выполнение скриптов
chmod +x scripts/*.sh

echo ""
echo "✅ Настройка завершена!"
echo ""
echo "Следующие шаги:"
echo "1. Отредактируйте файл .env с вашими настройками"
echo "2. Запустите бота: python run.py"
echo "3. Или используйте: ./scripts/start.sh"
echo ""
echo "Полезные команды:"
echo "- ./scripts/start.sh    - Запуск бота"
echo "- ./scripts/backup.sh   - Резервное копирование"
echo "- python run.py         - Прямой запуск"