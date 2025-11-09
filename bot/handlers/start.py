from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from datetime import timedelta
from pathlib import Path

from bot.keyboards.main_menu import main_menu, contacts_keyboard, gingerbread_types
from bot.utils.texts import BotTexts
from bot.utils.translations import get_text
from bot.utils.welcome_builder import build_welcome_message
from bot.utils.order_cache import order_cache
from bot.utils.context import get_user_lang
from database.crud import (get_or_create_customer, get_active_orders_by_customer,
                           update_customer_language, get_order_by_number)
from database.models import OrderStatus
from config.settings import settings, GINGERBREAD_TYPES

router = Router()


def language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk")
        ]
    ])
    return keyboard


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    """Обработчик команды /start"""
    await state.clear()

    # Создаем или получаем клиента
    customer = await get_or_create_customer(
        telegram_user_id=message.from_user.id,
        name=message.from_user.full_name
    )

    # Если язык не установлен, предлагаем выбрать
    if not customer.language:
        await message.answer(
            get_text("choose_language", "ru"),
            reply_markup=language_keyboard()
        )
        return

    # Получаем язык из контекста (кэш middleware)
    lang = get_user_lang(kwargs)

    # Проверяем кэш активных заказов
    active_orders = order_cache.get(customer.id)
    if active_orders is None:
        # Кэш пуст или устарел - загружаем из БД
        active_orders = await get_active_orders_by_customer(customer.id)
        order_cache.set(customer.id, active_orders)

    # Строим приветственное сообщение
    welcome_text, keyboard = build_welcome_message(
        customer, active_orders, lang, message.from_user.id
    )

    await message.answer(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext, **kwargs):
    """Возврат в главное меню"""
    await state.clear()

    # Получаем язык из контекста (кэш middleware)
    lang = get_user_lang(kwargs)

    # Получаем клиента и проверяем активные заказы
    customer = await get_or_create_customer(
        telegram_user_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    # Проверяем кэш активных заказов
    active_orders = order_cache.get(customer.id)
    if active_orders is None:
        # Кэш пуст или устарел - загружаем из БД
        active_orders = await get_active_orders_by_customer(customer.id)
        order_cache.set(customer.id, active_orders)

    # Строим приветственное сообщение
    welcome_text, keyboard = build_welcome_message(
        customer, active_orders, lang, callback.from_user.id
    )

    # Проверяем, есть ли у сообщения фото (возврат из карточки товара)
    if callback.message.photo:
        # Удаляем фото-сообщение и отправляем новое текстовое
        await callback.message.delete()
        await callback.message.answer(
            welcome_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        # Редактируем текстовое сообщение
        await callback.message.edit_text(
            welcome_text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    await callback.answer()


@router.callback_query(F.data == "catalog")
async def show_catalog(callback: CallbackQuery, **kwargs):
    """Показать каталог пряников"""
    lang = get_user_lang(kwargs)

    # Проверяем, есть ли у сообщения фото (возврат из карточки товара)
    if callback.message.photo:
        # Удаляем фото-сообщение и отправляем текстовое
        await callback.message.delete()
        await callback.message.answer(
            get_text("choose_type", lang),
            reply_markup=gingerbread_types(lang),
            parse_mode="Markdown"
        )
    else:
        # Просто редактируем текст
        await callback.message.edit_text(
            get_text("choose_type", lang),
            reply_markup=gingerbread_types(lang),
            parse_mode="Markdown"
        )

    await callback.answer()


@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery, **kwargs):
    """Показать контактную информацию"""
    lang = get_user_lang(kwargs)

    contacts_text = get_text("contacts", lang,
                            master_name=settings.master_name,
                            phone=settings.business_phone,
                            address=settings.pickup_address,
                            hours=settings.working_hours)

    await callback.message.edit_text(
        contacts_text,
        reply_markup=contacts_keyboard(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(Command("order"))
async def cmd_order(message: Message, state: FSMContext, **kwargs):
    """Команда для быстрого начала заказа"""
    from bot.states.order_states import OrderStates

    lang = get_user_lang(kwargs)

    await state.set_state(OrderStates.choosing_type)
    await message.answer(
        get_text("choose_type", lang),
        reply_markup=gingerbread_types(lang),
        parse_mode="Markdown"
    )


@router.message(Command("catalog"))
async def cmd_catalog(message: Message, **kwargs):
    """Команда для просмотра каталога"""
    lang = get_user_lang(kwargs)

    await message.answer(
        get_text("choose_type", lang),
        reply_markup=gingerbread_types(lang),
        parse_mode="Markdown"
    )


@router.message(Command("contacts"))
async def cmd_contacts(message: Message, **kwargs):
    """Команда для просмотра контактов"""
    lang = get_user_lang(kwargs)

    contacts_text = get_text("contacts", lang,
                            master_name=settings.master_name,
                            phone=settings.business_phone,
                            address=settings.pickup_address,
                            hours=settings.working_hours)

    await message.answer(
        contacts_text,
        reply_markup=contacts_keyboard(lang),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    """Установка языка пользователя"""
    lang = callback.data.split("_")[1]  # ru, en, uk

    # Сохраняем язык
    await update_customer_language(callback.from_user.id, lang)

    # Подтверждаем выбор
    await callback.message.edit_text(
        get_text("language_selected", lang)
    )

    # Получаем клиента и проверяем активные заказы
    customer = await get_or_create_customer(
        telegram_user_id=callback.from_user.id,
        name=callback.from_user.full_name
    )

    # Проверяем кэш активных заказов
    active_orders = order_cache.get(customer.id)
    if active_orders is None:
        # Кэш пуст или устарел - загружаем из БД
        active_orders = await get_active_orders_by_customer(customer.id)
        order_cache.set(customer.id, active_orders)

    # Строим приветственное сообщение
    welcome_text, keyboard = build_welcome_message(
        customer, active_orders, lang, callback.from_user.id
    )

    await callback.message.answer(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    await callback.answer()


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery):
    """Изменение языка"""
    await callback.message.edit_text(
        get_text("choose_language", "ru"),
        reply_markup=language_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("view_order_"))
async def view_order_details(callback: CallbackQuery, **kwargs):
    """Просмотр деталей заказа"""
    order_number = callback.data.replace("view_order_", "")
    lang = get_user_lang(kwargs)

    # Получаем заказ
    order = await get_order_by_number(order_number)

    if not order:
        await callback.answer(get_text("order_not_found", lang), show_alert=True)
        return

    # Проверяем, что заказ принадлежит пользователю
    if order.customer.telegram_user_id != callback.from_user.id:
        await callback.answer(get_text("order_not_found", lang), show_alert=True)
        return

    # Формируем детали заказа
    gingerbread_type = GINGERBREAD_TYPES.get(order.product_type, {})
    type_name = get_text(f"type_{order.product_type}", lang)

    # Статус заказа
    status_map = {
        "new": get_text("status_new", lang),
        "confirmed": get_text("status_confirmed", lang),
        "in_progress": get_text("status_in_progress", lang),
        "ready": get_text("status_ready", lang),
        "completed": get_text("status_completed", lang),
        "cancelled": get_text("status_cancelled", lang),
    }
    status_text = status_map.get(order.status, order.status)

    # Формируем тему если есть
    theme_line = ""
    if order.theme_description:
        theme_line = f"🎨 {get_text('theme_label', lang)}: {order.theme_description}\n"

    details_text = get_text(
        "order_details",
        lang,
        order_number=order.order_number,
        status=status_text,
        type=type_name,
        theme=theme_line,
        quantity=order.quantity,
        date=order.delivery_date.strftime("%d.%m.%Y"),
        occasion=order.occasion or get_text("no_occasion", lang),
        phone=order.phone,
        total=f"{order.total_price:.2f}",
        created=order.created_at.strftime("%d.%m.%Y %H:%M")
    )

    # Кнопка назад
    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_menu")]
    ])

    await callback.message.edit_text(
        details_text,
        reply_markup=back_button,
        parse_mode="Markdown"
    )
    await callback.answer()