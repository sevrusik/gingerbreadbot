"""
Кэш для активных заказов клиентов.
Снижает нагрузку на БД при частых обращениях к истории заказов.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from database.models import Order


class OrderCache:
    """Кэш активных заказов с TTL"""

    def __init__(self, ttl_seconds: int = 60):
        """
        Args:
            ttl_seconds: Время жизни кэша в секундах (по умолчанию 60 сек)
        """
        self._cache = {}  # {customer_id: (orders, timestamp)}
        self._ttl = timedelta(seconds=ttl_seconds)

    def get(self, customer_id: int) -> Optional[List[Order]]:
        """
        Получить заказы из кэша

        Args:
            customer_id: ID клиента

        Returns:
            Список заказов если есть в кэше и не устарел, иначе None
        """
        if customer_id not in self._cache:
            return None

        orders, timestamp = self._cache[customer_id]

        # Проверяем актуальность
        if datetime.now() - timestamp > self._ttl:
            del self._cache[customer_id]
            return None

        return orders

    def set(self, customer_id: int, orders: List[Order]) -> None:
        """
        Сохранить заказы в кэш

        Args:
            customer_id: ID клиента
            orders: Список заказов
        """
        self._cache[customer_id] = (orders, datetime.now())

    def invalidate(self, customer_id: int) -> None:
        """
        Инвалидировать кэш для клиента

        Args:
            customer_id: ID клиента
        """
        if customer_id in self._cache:
            del self._cache[customer_id]

    def clear(self) -> None:
        """Очистить весь кэш"""
        self._cache.clear()

    def cleanup(self) -> None:
        """Удалить устаревшие записи из кэша"""
        now = datetime.now()
        expired = [
            customer_id
            for customer_id, (_, timestamp) in self._cache.items()
            if now - timestamp > self._ttl
        ]

        for customer_id in expired:
            del self._cache[customer_id]


# Глобальный экземпляр кэша заказов
order_cache = OrderCache(ttl_seconds=60)
