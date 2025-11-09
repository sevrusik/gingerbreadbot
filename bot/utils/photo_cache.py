"""
Кэш для Telegram file_id фотографий пряников.
Позволяет избежать повторной загрузки файлов с диска.
"""

# Глобальный словарь для хранения file_id по типам пряников
photo_cache = {}


def get_cached_photo(type_key: str) -> str | None:
    """
    Получить file_id из кэша по типу пряника

    Args:
        type_key: Ключ типа пряника (classic, coloring, numbers, themed, urgent)

    Returns:
        file_id если есть в кэше, иначе None
    """
    return photo_cache.get(type_key)


def cache_photo(type_key: str, file_id: str) -> None:
    """
    Сохранить file_id в кэш

    Args:
        type_key: Ключ типа пряника
        file_id: Telegram file_id фотографии
    """
    photo_cache[type_key] = file_id


def clear_cache() -> None:
    """Очистить весь кэш"""
    photo_cache.clear()
