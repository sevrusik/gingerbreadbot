"""
Утилиты для работы с контекстом handler'ов
"""

from typing import Dict, Any


def get_user_lang(data: Dict[str, Any]) -> str:
    """
    Получить язык пользователя из контекста handler'а

    Args:
        data: Контекст handler'а (передается через **kwargs или как параметр)

    Returns:
        Код языка ('ru', 'en', 'uk'). По умолчанию 'ru'.

    Examples:
        >>> async def my_handler(message: Message, **kwargs):
        >>>     lang = get_user_lang(kwargs)
        >>>     text = get_text("welcome", lang)
    """
    return data.get('user_lang', 'ru')
