"""
Вспомогательные функции для работы с медиа-контентом
"""
import os
from pathlib import Path
from typing import Optional, List
from aiogram.types import FSInputFile, InputMediaPhoto


def get_example_image_path(gingerbread_type: str) -> Optional[str]:
    """
    Получить путь к изображению-примеру для типа пряника

    Args:
        gingerbread_type: Тип пряника (classic, coloring, numbers, themed, urgent)

    Returns:
        Полный путь к изображению или None если не найдено
    """
    # Список возможных расширений
    extensions = ['.jpg', '.jpeg', '.png', '.webp']

    # Базовая директория проекта (2 уровня выше от bot/utils)
    base_dir = Path(__file__).parent.parent.parent
    examples_dir = base_dir / 'media' / 'examples'

    # Проверяем наличие файла с разными расширениями
    for ext in extensions:
        image_path = examples_dir / f"{gingerbread_type}{ext}"
        if image_path.exists():
            return str(image_path)

    return None


def has_example_image(gingerbread_type: str) -> bool:
    """
    Проверить, есть ли изображение-пример для типа пряника

    Args:
        gingerbread_type: Тип пряника

    Returns:
        True если изображение есть, False если нет
    """
    return get_example_image_path(gingerbread_type) is not None


def get_all_example_images() -> List[tuple[str, str]]:
    """
    Получить список всех доступных изображений-примеров

    Returns:
        Список кортежей (тип_пряника, путь_к_файлу)
    """
    types = ['classic', 'coloring', 'numbers', 'themed', 'urgent']
    images = []

    for gingerbread_type in types:
        path = get_example_image_path(gingerbread_type)
        if path:
            images.append((gingerbread_type, path))

    return images


def create_media_group_from_types(types_list: List[str], caption: str = "") -> List[InputMediaPhoto]:
    """
    Создать медиа-группу из изображений для указанных типов пряников

    Args:
        types_list: Список типов пряников
        caption: Подпись для первого фото (опционально)

    Returns:
        Список InputMediaPhoto для отправки медиа-группы
    """
    media_group = []

    for idx, gingerbread_type in enumerate(types_list):
        image_path = get_example_image_path(gingerbread_type)
        if image_path:
            # Подпись только для первого фото
            photo_caption = caption if idx == 0 else ""
            media_group.append(
                InputMediaPhoto(
                    media=FSInputFile(image_path),
                    caption=photo_caption,
                    parse_mode="Markdown"
                )
            )

    return media_group
