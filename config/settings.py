import os
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Telegram Bot
    telegram_bot_token: str
    admin_user_ids: str  # Comma-separated list of admin IDs

    # Database
    database_url: str = "sqlite:///./database/orders.db"

    # App
    debug: bool = False
    log_level: str = "INFO"
    webhook_url: str = ""
    webhook_path: str = "/webhook"
    webapp_host: str = "0.0.0.0"
    webapp_port: int = 8080

    # Business
    master_name: str = "Любовь"
    business_phone: str = ""
    pickup_address: str = ""
    pickup_coordinates: str = ""
    working_hours: str = "10:00-12:00, 18:00-20:00"

    # Pricing
    base_price_eur: float = 2.0
    coloring_price_eur: float = 12.0  # Набор из 3 пряников с красками
    topper_price_eur: float = 5.0  # Минимальная цена топера
    rush_order_multiplier: float = 1.25
    min_preparation_days: int = 10
    min_preparation_days_urgent: int = 3

    # Quantity limits
    min_quantity: int = 10  # Минимум для обычных пряников
    min_quantity_topper: int = 1  # Минимум для топеров
    coloring_set_size: int = 3  # Количество пряников в наборе-раскраске

    # Google Calendar
    google_calendar_enabled: bool = False
    google_calendar_id: str = "primary"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def admin_ids_list(self) -> List[int]:
        """Возвращает список ID администраторов"""
        return [int(id.strip()) for id in self.admin_user_ids.split(',') if id.strip()]

    def is_admin(self, user_id: int) -> bool:
        """Проверяет является ли пользователь администратором"""
        return user_id in self.admin_ids_list


# Создаем глобальный экземпляр настроек
settings = Settings()


# Список типов пряников
GINGERBREAD_TYPES = {
    "classic": {
        "name": "Классические расписные",
        "description": "Готовые пряники с красивой глазурью",
        "price": settings.base_price_eur,
        "emoji": "🍪",
        "is_urgent": False,
        "example_image": "media/examples/classic.jpg"
    },
    "coloring": {
        "name": "Пряники-раскраски",
        "description": "Набор из 3 пряников с палитрой красок и кисточкой",
        "price": settings.coloring_price_eur,
        "emoji": "🎨",
        "is_urgent": False,
        "is_set": True,  # Это набор, а не поштучно
        "set_size": settings.coloring_set_size,
        "example_image": "media/examples/coloring.jpg"
    },
    "numbers": {
        "name": "Цифры",
        "description": "Для дней рождения",
        "price": settings.base_price_eur,
        "emoji": "🔢",
        "is_urgent": False,
        "example_image": "media/examples/numbers.jpg"
    },
    "themed": {
        "name": "Тематические",
        "description": "По индивидуальному дизайну",
        "price": settings.base_price_eur,
        "emoji": "✨",
        "is_urgent": False,
        "example_image": "media/examples/themed.jpg"
    },
    "urgent": {
        "name": "Срочный заказ",
        "description": "Двойная стоимость, без минимального срока",
        "price": settings.base_price_eur * 2,
        "emoji": "🚨",
        "is_urgent": True,
        "example_image": "media/examples/urgent.jpg"
    },
    "topper": {
        "name": "Топер для торта",
        "description": "Большой пряник 10×15 см для украшения торта",
        "price": settings.topper_price_eur,
        "emoji": "🎂",
        "is_urgent": False,
        "min_quantity": settings.min_quantity_topper,
        "example_image": "media/examples/topper.png"
    }
}

# Популярные темы (мультиязычные)
POPULAR_THEMES_TRANSLATIONS = {
    "unicorns": {"ru": "Единороги", "en": "Unicorns", "uk": "Єдинороги"},
    "dinosaurs": {"ru": "Динозавры", "en": "Dinosaurs", "uk": "Динозаври"},
    "princesses": {"ru": "Принцессы", "en": "Princesses", "uk": "Принцеси"},
    "cars": {"ru": "Машинки", "en": "Cars", "uk": "Машинки"},
    "animals": {"ru": "Животные", "en": "Animals", "uk": "Тварини"},
    "flowers": {"ru": "Цветы", "en": "Flowers", "uk": "Квіти"},
    "space": {"ru": "Космос", "en": "Space", "uk": "Космос"},
    "cartoons": {"ru": "Мультики", "en": "Cartoons", "uk": "Мультики"}
}

# Старый формат для обратной совместимости
POPULAR_THEMES = [
    "Единороги", "Динозавры", "Принцессы", "Машинки",
    "Животные", "Цветы", "Космос", "Мультики"
]