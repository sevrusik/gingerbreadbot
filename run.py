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

# Проверяем наличие .env файла
env_file = ROOT_DIR / ".env"
if not env_file.exists():
    print("❌ Файл .env не найден!")
    print("Создайте файл .env с настройками по примеру:")
    print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
    print("ADMIN_USER_ID=your_telegram_user_id")
    sys.exit(1)

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