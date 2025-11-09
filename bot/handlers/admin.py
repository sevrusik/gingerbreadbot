from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from datetime import datetime, timedelta

from config.settings import settings
from bot.keyboards.main_menu import admin_menu
from bot.utils.order_cache import order_cache
from bot.utils.context import get_user_lang
from database.crud import (
    get_active_orders, get_orders_by_date, get_daily_stats,
    update_order_status, get_order_by_number
)
from database.models import OrderStatus

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка прав администратора"""
    return settings.is_admin(user_id)


@router.message(Command("reset_commands"))
async def reset_my_commands(message: Message):
    """Сброс команд бота для текущего пользователя (возврат к дефолтным)"""
    from bot.main import bot
    from aiogram.types import BotCommandScopeChat

    try:
        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=message.from_user.id))
        await message.answer("✅ Команды сброшены. Пожалуйста, перезапустите чат с ботом (закройте и откройте снова).")
    except Exception as e:
        await message.answer(f"❌ Ошибка при сбросе команд: {e}")


@router.message(Command("admin"))
async def admin_panel(message: Message, **kwargs):
    """Админская панель"""
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав администратора")
        return

    lang = get_user_lang(kwargs)
    await message.answer(
        "🔧 **Админская панель**\n\nВыберите действие:",
        reply_markup=admin_menu(lang),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, **kwargs):
    """Админская панель через callback"""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔️ Недостаточно прав", show_alert=True)
        return

    lang = get_user_lang(kwargs)
    await callback.message.edit_text(
        "🔧 **Админская панель**\n\nВыберите действие:",
        reply_markup=admin_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_orders")
async def show_active_orders(callback: CallbackQuery, **kwargs):
    """Показать активные заказы"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    lang = get_user_lang(kwargs)
    orders = await get_active_orders()

    if not orders:
        await callback.message.edit_text(
            "📝 Активных заказов нет",
            reply_markup=admin_menu(lang)
        )
        await callback.answer()
        return

    text = "📋 **Активные заказы:**\n\n"
    buttons = []

    for order in orders[:10]:  # Показываем первые 10
        status_emoji = {
            "new": "🆕",
            "confirmed": "✅",
            "in_progress": "⚙️",
            "ready": "🎁"
        }.get(order.status, "❓")

        text += f"{status_emoji} **#{order.order_number}**\n"
        text += f"📦 {order.quantity} × {order.product_type}\n"
        text += f"📅 {order.delivery_date.strftime('%d.%m.%Y')}\n"
        text += f"💰 {order.total_price}€\n"
        text += f"📞 {order.phone}\n\n"

        # Добавляем кнопки для каждого заказа
        buttons.append([
            InlineKeyboardButton(
                text=f"❌ Отменить #{order.order_number}",
                callback_data=f"cancel_order_{order.order_number}"
            )
        ])

    if len(orders) > 10:
        text += f"... и еще {len(orders) - 10} заказов"

    # Добавляем кнопку "Назад"
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin_back")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_calendar")
async def show_calendar(callback: CallbackQuery, **kwargs):
    """Показать календарь заказов"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    lang = get_user_lang(kwargs)
    today = datetime.now()
    text = "📅 **Календарь заказов на ближайшие дни:**\n\n"

    for i in range(7):  # Показываем 7 дней
        date = today + timedelta(days=i)
        orders = await get_orders_by_date(date)

        date_str = date.strftime("%d.%m (%a)")
        if i == 0:
            date_str += " - Сегодня"
        elif i == 1:
            date_str += " - Завтра"

        total_items = sum(order.quantity for order in orders)
        total_revenue = sum(order.total_price for order in orders)

        text += f"📅 **{date_str}**\n"
        text += f"📦 Заказов: {len(orders)} ({total_items} шт)\n"
        text += f"💰 Выручка: {total_revenue}€\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def show_statistics(callback: CallbackQuery, **kwargs):
    """Показать статистику"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    lang = get_user_lang(kwargs)
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Статистика за сегодня
    today_stats = await get_daily_stats(today)

    # Статистика за неделю
    week_orders = []
    for i in range(7):
        date = today - timedelta(days=i)
        day_orders = await get_orders_by_date(date)
        week_orders.extend(day_orders)

    week_revenue = sum(order.total_price for order in week_orders)
    week_items = sum(order.quantity for order in week_orders)

    text = f"""📊 **Статистика**

**Сегодня ({today.strftime('%d.%m')}):**
📦 Заказов: {today_stats['total_orders']}
🍪 Пряников: {today_stats['total_items']} шт
💰 Выручка: {today_stats['total_revenue']}€

**За неделю:**
📦 Заказов: {len(week_orders)}
🍪 Пряников: {week_items} шт
💰 Выручка: {week_revenue}€

**Средний чек:** {(week_revenue / len(week_orders) if week_orders else 0):.1f}€
**Средний заказ:** {(week_items / len(week_orders) if week_orders else 0):.1f} шт"""

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(Command("status"))
async def change_order_status(message: Message):
    """Изменение статуса заказа"""
    if not is_admin(message.from_user.id):
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer(
            "Использование: /status <номер_заказа> <статус>\n\n"
            "Статусы: new, confirmed, in_progress, ready, completed, cancelled"
        )
        return
    
    order_number = args[1]
    status_str = args[2]
    
    # Проверяем статус
    try:
        status = OrderStatus(status_str)
    except ValueError:
        await message.answer("Неверный статус. Доступные: new, confirmed, in_progress, ready, completed, cancelled")
        return
    
    # Ищем заказ
    order = await get_order_by_number(order_number)
    if not order:
        await message.answer(f"Заказ #{order_number} не найден")
        return
    
    # Обновляем статус
    await update_order_status(order.id, status)

    # Инвалидируем кэш заказов клиента
    order_cache.invalidate(order.customer.id)

    status_names = {
        OrderStatus.NEW: "Новый",
        OrderStatus.CONFIRMED: "Подтвержден",
        OrderStatus.IN_PROGRESS: "В работе",
        OrderStatus.READY: "Готов",
        OrderStatus.COMPLETED: "Выполнен",
        OrderStatus.CANCELLED: "Отменен"
    }

    await message.answer(f"✅ Статус заказа #{order_number} изменен на: {status_names[status]}")


@router.message(Command("today"))
async def today_orders(message: Message):
    """Заказы на сегодня"""
    if not is_admin(message.from_user.id):
        return
    
    today = datetime.now()
    orders = await get_orders_by_date(today)
    
    if not orders:
        await message.answer("📝 На сегодня заказов нет")
        return
    
    text = f"📅 **Заказы на {today.strftime('%d.%m.%Y')}:**\n\n"
    
    for order in orders:
        status_emoji = {
            "new": "🆕",
            "confirmed": "✅",
            "in_progress": "⚙️", 
            "ready": "🎁",
            "completed": "✅",
            "cancelled": "❌"
        }.get(order.status, "❓")
        
        text += f"{status_emoji} **#{order.order_number}**\n"
        text += f"🍪 {order.quantity} × {order.product_type}\n"
        if order.theme_description:
            text += f"🎨 {order.theme_description}\n"
        text += f"🎉 {order.occasion}\n"
        text += f"📞 {order.phone}\n"
        text += f"💰 {order.total_price}€\n\n"
    
    total_items = sum(order.quantity for order in orders)
    total_revenue = sum(order.total_price for order in orders)
    text += f"**Итого:** {len(orders)} заказов, {total_items} пряников, {total_revenue}€"
    
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("tomorrow"))
async def tomorrow_orders(message: Message):
    """Заказы на завтра"""
    if not is_admin(message.from_user.id):
        return
    
    tomorrow = datetime.now() + timedelta(days=1)
    orders = await get_orders_by_date(tomorrow)
    
    if not orders:
        await message.answer("📝 На завтра заказов нет")
        return
    
    text = f"📅 **Заказы на {tomorrow.strftime('%d.%m.%Y')}:**\n\n"
    
    for order in orders:
        text += f"🆕 **#{order.order_number}**\n"
        text += f"🍪 {order.quantity} × {order.product_type}\n"
        if order.theme_description:
            text += f"🎨 {order.theme_description}\n"
        text += f"🎉 {order.occasion}\n"
        text += f"📞 {order.phone}\n"
        text += f"💰 {order.total_price}€\n\n"
    
    total_items = sum(order.quantity for order in orders)
    total_revenue = sum(order.total_price for order in orders)
    text += f"**Итого:** {len(orders)} заказов, {total_items} пряников, {total_revenue}€"
    
    await message.answer(text, parse_mode="Markdown")

@router.callback_query(F.data == "admin_back")
async def admin_back(callback: CallbackQuery, **kwargs):
    """Возврат в админское меню"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    lang = get_user_lang(kwargs)
    await callback.message.edit_text(
        "🔧 **Админская панель**\n\nВыберите действие:",
        reply_markup=admin_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order_confirm(callback: CallbackQuery):
    """Подтверждение отмены заказа"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_number = callback.data.replace("cancel_order_", "")
    order = await get_order_by_number(order_number)

    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    # Показываем подтверждение
    text = f"""❓ **Отменить заказ #{order.order_number}?**

📦 {order.quantity} × {order.product_type}
📅 {order.delivery_date.strftime('%d.%m.%Y')}
💰 {order.total_price}€
📞 {order.phone}

⚠️ Это действие нельзя отменить!"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, отменить", callback_data=f"cancel_confirmed_{order_number}"),
            InlineKeyboardButton(text="❌ Нет", callback_data="admin_orders")
        ]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_confirmed_"))
async def cancel_order_execute(callback: CallbackQuery):
    """Выполнение отмены заказа"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_number = callback.data.replace("cancel_confirmed_", "")
    order = await get_order_by_number(order_number)

    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    # Обновляем статус заказа на "cancelled"
    await update_order_status(order.id, OrderStatus.CANCELLED)

    # Инвалидируем кэш заказов клиента
    order_cache.invalidate(order.customer.id)

    # Уведомляем администратора
    await callback.message.edit_text(
        f"✅ Заказ #{order_number} отменен",
        parse_mode="Markdown"
    )

    # Уведомляем клиента об отмене
    try:
        from bot.main import bot
        await bot.send_message(
            chat_id=order.customer.telegram_user_id,
            text=f"""❌ **Ваш заказ #{order_number} отменен**

К сожалению, заказ был отменен администратором.

📞 **Что делать дальше?**
• Свяжитесь с нами через раздел "Контакты" для уточнения причин
• Вы можете оформить новый заказ в любое время

Приносим извинения за неудобства.""",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Не удалось уведомить клиента об отмене: {e}")

    await callback.answer("Заказ отменен", show_alert=True)

    # Возвращаемся к списку заказов через 2 секунды
    import asyncio
    await asyncio.sleep(2)
    await show_active_orders(callback)


@router.callback_query(F.data.startswith("approve_order_"))
async def approve_order(callback: CallbackQuery):
    """Подтверждение заказа администратором"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_number = callback.data.replace("approve_order_", "")
    order = await get_order_by_number(order_number)

    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    # Обновляем статус заказа на "confirmed"
    await update_order_status(order.id, OrderStatus.CONFIRMED)

    # Инвалидируем кэш заказов клиента
    order_cache.invalidate(order.customer.id)

    # Обновляем сообщение админу
    await callback.message.edit_text(
        callback.message.text.replace("⏳ **Ожидает подтверждения**", "✅ **ПОДТВЕРЖДЕН**"),
        parse_mode="Markdown"
    )

    # Уведомляем клиента о подтверждении
    try:
        from bot.main import bot
        from bot.utils.translations import get_text

        # Получаем язык клиента
        customer_lang = order.customer.language or "ru"

        # Формируем текст уведомления
        notification_text = get_text(
            "order_confirmed_by_master",
            customer_lang,
            order_number=order_number,
            date=order.delivery_date.strftime('%d.%m.%Y'),
            total=f"{order.total_price:.2f}"
        )

        await bot.send_message(
            chat_id=order.customer.telegram_user_id,
            text=notification_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Не удалось уведомить клиента о подтверждении: {e}")

    await callback.answer("✅ Заказ подтвержден!", show_alert=True)


@router.callback_query(F.data.startswith("reject_order_"))
async def reject_order(callback: CallbackQuery):
    """Отклонение заказа администратором"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    order_number = callback.data.replace("reject_order_", "")
    order = await get_order_by_number(order_number)

    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    # Обновляем статус заказа на "cancelled"
    await update_order_status(order.id, OrderStatus.CANCELLED)

    # Инвалидируем кэш заказов клиента
    order_cache.invalidate(order.customer.id)

    # Обновляем сообщение админу
    await callback.message.edit_text(
        callback.message.text.replace("⏳ **Ожидает подтверждения**", "❌ **ОТКЛОНЕН**"),
        parse_mode="Markdown"
    )

    # Уведомляем клиента об отклонении
    try:
        from bot.main import bot
        await bot.send_message(
            chat_id=order.customer.telegram_user_id,
            text=f"""😔 **Ваш заказ #{order_number} не может быть выполнен**

К сожалению, мастер не может принять ваш заказ.
Возможные причины:
- Недостаточно времени на изготовление
- Слишком большая загрузка
- Технические ограничения

Пожалуйста, свяжитесь с нами для уточнения деталей или попробуйте оформить заказ на другую дату.""",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Не удалось уведомить клиента об отклонении: {e}")

    await callback.answer("❌ Заказ отклонен", show_alert=True)
