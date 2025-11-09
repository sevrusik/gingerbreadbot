import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from config.settings import settings
from database.crud import init_db
from bot.handlers import start, order, admin
from bot.middlewares import LanguageMiddleware

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def setup_bot_commands():
    """Настройка команд бота в меню"""
    # Команды для обычных пользователей
    user_commands = [
        BotCommand(command="start", description="🍪 Домой, к тёплым пряникам"),
        BotCommand(command="order", description="👩‍🍳 Заказать набор пряников"),
        BotCommand(command="catalog", description="📖 Посмотреть ароматный каталог"),
        BotCommand(command="contacts", description="💌 Связаться с мастером"),
    ]

    # Команды для администраторов
    admin_commands = [
        BotCommand(command="start", description="🍪 Домой, к тёплым пряникам"),
        BotCommand(command="admin", description="🔧 Админ панель"),
        BotCommand(command="today", description="📅 Заказы на сегодня"),
        BotCommand(command="tomorrow", description="📅 Заказы на завтра"),
        BotCommand(command="status", description="🔄 Изменить статус заказа"),
    ]

    # Устанавливаем команды по умолчанию для всех пользователей
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
    logger.info("Команды для пользователей установлены")

    # Устанавливаем команды для каждого администратора
    for admin_id in settings.admin_ids_list:
        try:
            await bot.set_my_commands(
                admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
            logger.info(f"Команды для администратора {admin_id} установлены")
        except Exception as e:
            logger.error(f"Не удалось установить команды для админа {admin_id}: {e}")


async def reset_user_commands(user_id: int):
    """Сброс команд для конкретного пользователя (возврат к дефолтным)"""
    try:
        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=user_id))
        logger.info(f"Команды сброшены для пользователя {user_id}")
    except Exception as e:
        logger.error(f"Не удалось сбросить команды для пользователя {user_id}: {e}")


async def on_startup():
    """Действия при запуске бота"""
    logger.info("Запуск бота...")

    # Инициализация базы данных
    await init_db()
    logger.info("База данных инициализирована")

    # Настройка команд бота
    await setup_bot_commands()
    logger.info("Команды бота настроены")

    # Уведомляем всех админов о запуске
    for admin_id in settings.admin_ids_list:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🤖 Бот запущен и готов к работе!"
            )
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление админу {admin_id}: {e}")


async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("Остановка бота...")

    # Уведомляем всех админов об остановке
    for admin_id in settings.admin_ids_list:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text="🔴 Бот остановлен"
            )
        except Exception as e:
            logger.error(f"Не удалось отправить уведомление об остановке админу {admin_id}: {e}")


def register_handlers():
    """Регистрация обработчиков"""
    # Регистрируем middleware для кэширования языка
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())
    logger.info("Language middleware зарегистрирован")

    # Регистрируем роутеры в правильном порядке
    dp.include_router(start.router)
    dp.include_router(order.router)
    dp.include_router(admin.router)

    logger.info("Обработчики зарегистрированы")


async def main():
    """Основная функция запуска бота"""
    # Регистрируем обработчики
    register_handlers()
    
    # Регистрируем события
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info("Начинаем polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise