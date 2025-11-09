"""
Построитель приветственных сообщений для различных сценариев.
Устраняет дублирование кода в start.py
"""

from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Order, Customer
from bot.keyboards.main_menu import main_menu
from bot.utils.translations import get_text
from config.settings import settings


def build_welcome_message(
    customer: Customer,
    active_orders: List[Order],
    lang: str,
    user_id: int
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Построить приветственное сообщение с учетом активных заказов

    Args:
        customer: Объект клиента
        active_orders: Список активных заказов
        lang: Код языка пользователя
        user_id: Telegram ID пользователя

    Returns:
        Кортеж (текст сообщения, клавиатура)
    """
    if active_orders:
        # Персонализированное приветствие для клиентов с активными заказами
        welcome_text = get_text("welcome_with_orders", lang)

        # Добавляем информацию об активных заказах
        orders_info = "\n\n" + get_text("my_orders_header", lang) + "\n"

        # Создаем inline кнопки для каждого заказа
        order_buttons = []
        for order in active_orders:
            delivery_date_str = order.delivery_date.strftime("%d.%m.%Y")
            status_emoji = "🟢" if order.status == "confirmed" else "🟡"
            orders_info += f"{status_emoji} #{order.order_number} - {delivery_date_str}\n"

            # Добавляем кнопку для просмотра деталей
            order_buttons.append([
                InlineKeyboardButton(
                    text=f"📋 #{order.order_number}",
                    callback_data=f"view_order_{order.order_number}"
                )
            ])

        welcome_text = welcome_text + orders_info

        # Добавляем кнопки заказов к главному меню
        main_menu_kb = main_menu(lang, user_id)
        combined_kb = InlineKeyboardMarkup(
            inline_keyboard=order_buttons + main_menu_kb.inline_keyboard
        )

        return welcome_text, combined_kb
    else:
        # Обычное приветствие для новых клиентов
        welcome_text = get_text("welcome", lang, master_name=settings.master_name)
        keyboard = main_menu(lang, user_id)

        return welcome_text, keyboard
