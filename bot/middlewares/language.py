"""
Middleware для кэширования языка пользователя.
Загружает язык один раз при обработке update и сохраняет в контексте.
Это избегает повторных запросов к БД в каждом handler'е.
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from database.crud import get_customer_language


class LanguageMiddleware(BaseMiddleware):
    """
    Middleware для кэширования языка пользователя в контексте обработки update.

    Загружает язык из БД один раз и сохраняет в data['user_lang'].
    После этого все handlers могут использовать data.get('user_lang', 'ru').
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обработка update с кэшированием языка

        Args:
            handler: Следующий обработчик в цепочке
            event: Входящий update (Message, CallbackQuery, и т.д.)
            data: Контекст обработки
        """
        # Получаем user_id из разных типов event
        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None
        else:
            # Для других типов пытаемся получить из event
            if hasattr(event, 'from_user') and event.from_user:
                user_id = event.from_user.id

        # Загружаем язык из БД и кэшируем в контексте
        if user_id:
            lang = await get_customer_language(user_id)
            data['user_lang'] = lang
        else:
            # Дефолтный язык если не смогли определить пользователя
            data['user_lang'] = 'ru'

        # Передаем управление следующему обработчику
        return await handler(event, data)
