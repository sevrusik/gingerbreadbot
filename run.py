#!/usr/bin/env python3
"""
Точка входа для запуска Telegram-бота для заказа пряников
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Проверяем обязательные переменные окружения
# Файл .env используется локально и Docker Compose, но не копируется в образ
if not os.getenv("TELEGRAM_BOT_TOKEN"):
    print("❌ Переменная окружения TELEGRAM_BOT_TOKEN не установлена!")
    print("Для локальной разработки создайте файл .env с настройками:")
    print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
    print("ADMIN_USER_IDS=your_telegram_user_id")
    print("\nДля Docker переменные передаются через env_file в docker-compose.yml")
    sys.exit(1)

# Определяем режим работы
env_file = ROOT_DIR / ".env"
if env_file.exists():
    print("ℹ️  Локальная разработка (используется .env файл)")
else:
    print("ℹ️  Production mode (переменные окружения из Docker)")

# Импортируем и запускаем бота
if __name__ == "__main__":
    try:
        from bot.main import main
        import asyncio
        
        print("🍪 Запуск бота для заказа пряников...")
        asyncio.run(main())
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        import traceback
        print(f"❌ Критическая ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)