from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from pathlib import Path
import re

from bot.states.order_states import OrderStates
from bot.keyboards.main_menu import gingerbread_types, popular_themes, confirmation_keyboard, phone_keyboard, main_menu
from bot.utils.texts import BotTexts
from bot.utils.translations import get_text
from bot.utils.validators import validate_phone, validate_date, parse_date, escape_markdown
from bot.utils.media_helper import get_all_example_images, create_media_group_from_types
from bot.utils.photo_cache import get_cached_photo, cache_photo
from bot.utils.order_cache import order_cache
from bot.utils.context import get_user_lang
from config.settings import GINGERBREAD_TYPES, settings
from database.crud import create_order, get_customer_by_telegram_id, check_date_availability

router = Router()




@router.callback_query(F.data.startswith("type_"))
async def choose_type(callback: CallbackQuery, state: FSMContext, **kwargs):
    """Выбор типа пряников - показываем карточку с примером"""
    type_key = callback.data.split("_")[1]
    type_data = GINGERBREAD_TYPES[type_key]

    lang = get_user_lang(kwargs)
    type_name = get_text(f"type_{type_key}", lang)

    # Для типов с подтипами цена будет установлена позже при выборе подтипа
    initial_price = type_data.get("price", 0.0)

    await state.update_data(
        type=type_key,
        type_name=type_name,
        price_per_item=initial_price,
        is_urgent=type_data.get("is_urgent", False),
        lang=lang
    )

    # Путь к файлу примера
    example_path = Path(f"media/examples/{type_key}.png")
    if not example_path.exists():
        example_path = Path(f"media/examples/{type_key}.jpg")

    # Получаем описание на нужном языке
    description = get_text(f"type_{type_key}_desc", lang)

    # Текст для метки цены на нужном языке
    price_label = {"ru": "Цена", "en": "Price", "uk": "Ціна"}
    price_from = get_text("price_from", lang)

    # Формируем текст карточки
    if type_data.get("has_subtypes"):
        # Для типов с подтипами показываем диапазон цен
        prices = [subtype["price"] for subtype in type_data["subtypes"].values()]
        min_price = min(prices)
        max_price = max(prices)
        if min_price == max_price:
            price_text = f"{price_from} {min_price}€"
        else:
            price_text = f"{price_from} {min_price}-{max_price}€"
        card_text = f"🍪 **{type_name}**\n\n{description}\n\n💰 {price_label.get(lang, 'Цена')}: {price_text}"
    else:
        # Для обычных типов показываем цену за штуку
        card_text = f"🍪 **{type_name}**\n\n{description}\n\n💰 {price_label.get(lang, 'Цена')}: {price_from} {initial_price}€/шт"

    # Кнопки для карточки товара
    order_btn_text = get_text("btn_order_this", lang)
    back_btn_text = get_text("btn_back_to_selection", lang)

    continue_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=order_btn_text, callback_data=f"continue_{type_key}")],
        [InlineKeyboardButton(text=back_btn_text, callback_data="view_and_order")]
    ])

    # Удаляем предыдущее сообщение и отправляем фото с описанием
    await callback.message.delete()

    if example_path.exists():
        # Проверяем кэш
        cached_file_id = get_cached_photo(type_key)

        if cached_file_id:
            # Используем закэшированный file_id
            sent_message = await callback.message.answer_photo(
                photo=cached_file_id,
                caption=card_text,
                reply_markup=continue_keyboard,
                parse_mode="Markdown"
            )
        else:
            # Загружаем файл и кэшируем file_id
            photo = FSInputFile(example_path)
            sent_message = await callback.message.answer_photo(
                photo=photo,
                caption=card_text,
                reply_markup=continue_keyboard,
                parse_mode="Markdown"
            )
            # Сохраняем file_id в кэш
            if sent_message.photo:
                file_id = sent_message.photo[-1].file_id  # Берем самое большое фото
                cache_photo(type_key, file_id)
    else:
        # Если нет фото - просто текст
        await callback.message.answer(
            card_text,
            reply_markup=continue_keyboard,
            parse_mode="Markdown"
        )

    await callback.answer()


@router.callback_query(F.data.startswith("continue_"))
async def continue_order_after_preview(callback: CallbackQuery, state: FSMContext):
    """Продолжение заказа после просмотра карточки"""
    type_key = callback.data.split("_")[1]
    data = await state.get_data()
    lang = data.get("lang", "ru")

    # Удаляем фото-карточку
    await callback.message.delete()

    # Для типов с подтипами - показываем выбор подтипа
    type_data = GINGERBREAD_TYPES.get(type_key, {})
    if type_data.get("has_subtypes"):
        await state.set_state(OrderStates.choosing_subtype)

        # Создаем клавиатуру с подтипами
        subtypes_keyboard_buttons = []
        for subtype_key, subtype_data in type_data["subtypes"].items():
            button_text = f"{subtype_data['emoji']} {subtype_data['name']} ({subtype_data['price']} €)"
            callback_prefix = f"{type_key}_subtype_{subtype_key}"
            subtypes_keyboard_buttons.append([
                InlineKeyboardButton(text=button_text, callback_data=callback_prefix)
            ])

        subtypes_keyboard_buttons.append([
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_types")
        ])

        subtypes_keyboard = InlineKeyboardMarkup(inline_keyboard=subtypes_keyboard_buttons)

        prompt_key = f"choose_{type_key}_subtype" if type_key == "newyear" else "choose_coloring_subtype"
        await callback.message.answer(
            get_text(prompt_key, lang),
            reply_markup=subtypes_keyboard,
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    # Переходим к количеству
    await state.set_state(OrderStates.entering_quantity)

    # Для срочных заказов показываем предупреждение
    if type_key == "urgent":
        await callback.message.answer(
            get_text("urgent_order_info", lang),
            parse_mode="Markdown"
        )

    # Выбираем подходящий текст для запроса количества
    if type_key == "coloring":
        quantity_text = "enter_quantity_coloring"
    elif type_key == "topper":
        quantity_text = "enter_quantity_topper"
    else:
        quantity_text = "enter_quantity"

    await callback.message.answer(
        get_text(quantity_text, lang),
        parse_mode="Markdown"
    )

    await callback.answer()


@router.callback_query(F.data.contains("_subtype_"))
async def choose_subtype(callback: CallbackQuery, state: FSMContext):
    """Универсальный обработчик выбора подтипа"""
    # Парсим callback_data: "{type}_subtype_{subtype_key}"
    parts = callback.data.split("_subtype_")
    type_key = parts[0]
    subtype_key = parts[1]

    data = await state.get_data()
    lang = data.get("lang", "ru")

    type_data = GINGERBREAD_TYPES[type_key]
    subtype_data = type_data["subtypes"][subtype_key]

    # Сохраняем данные подтипа
    await state.update_data(
        subtype=subtype_key,
        subtype_name=subtype_data["name"],
        price_per_item=subtype_data["price"],
        set_size=subtype_data.get("set_size", 1)
    )

    await state.set_state(OrderStates.entering_quantity)

    # Формируем сообщение о выборе
    selection_msg = get_text("subtype_selected", lang,
                            subtype=subtype_data["name"],
                            price=subtype_data["price"])

    # Выбираем текст для запроса количества
    if type_key == "coloring":
        quantity_prompt = get_text("enter_quantity_coloring_subtype", lang)
    elif type_key == "newyear":
        quantity_prompt = get_text("enter_quantity_newyear", lang)
    else:
        quantity_prompt = get_text("enter_quantity", lang)

    await callback.message.edit_text(
        selection_msg + "\n\n" + quantity_prompt,
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("theme_"))
async def choose_theme(callback: CallbackQuery, state: FSMContext):
    """Выбор готовой темы"""
    from config.settings import POPULAR_THEMES_TRANSLATIONS

    theme_key = callback.data.split("_", 1)[1]
    data = await state.get_data()
    lang = data.get("lang", "ru")

    # Получаем название темы на нужном языке
    theme_name = POPULAR_THEMES_TRANSLATIONS.get(theme_key, {}).get(lang, theme_key)

    await state.update_data(theme=theme_name)

    await state.set_state(OrderStates.entering_quantity)
    theme_selected = {
        "ru": f"Выбрана тема: **{theme_name}** ✨\n\n",
        "en": f"Theme selected: **{theme_name}** ✨\n\n",
        "uk": f"Обрано тему: **{theme_name}** ✨\n\n"
    }
    await callback.message.edit_text(
        theme_selected.get(lang, theme_selected["ru"]) + get_text("enter_quantity", lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "custom_theme")
async def custom_theme(callback: CallbackQuery, state: FSMContext):
    """Выбор своей темы"""
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.set_state(OrderStates.choosing_theme)
    await callback.message.edit_text(
        get_text("custom_theme", lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_types")
async def back_to_types(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору типа пряников"""
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.set_state(OrderStates.choosing_type)
    await callback.message.edit_text(
        get_text("choose_type", lang),
        reply_markup=gingerbread_types(lang),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.message(OrderStates.choosing_theme)
async def process_custom_theme(message: Message, state: FSMContext):
    """Обработка пользовательской темы"""
    theme = message.text.strip()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.update_data(theme=theme)

    await state.set_state(OrderStates.entering_quantity)
    await message.answer(
        get_text("theme_recorded", lang, theme=theme) + get_text("enter_quantity", lang),
        parse_mode="Markdown"
    )


@router.message(OrderStates.entering_quantity)
async def process_quantity(message: Message, state: FSMContext):
    """Обработка количества"""
    data = await state.get_data()
    lang = data.get("lang", "ru")
    product_type = data.get("type")

    try:
        quantity = int(message.text.strip())
    except ValueError:
        await message.answer(get_text("invalid_quantity", lang))
        return

    # Определяем минимальное и максимальное количество в зависимости от типа
    if product_type == "coloring":
        # Для раскрасок с подтипами - используем set_size из подтипа
        set_size = data.get("set_size", 1)
        min_qty = 1
        max_qty = 100
        if quantity < min_qty or quantity > max_qty:
            await message.answer(
                get_text("invalid_quantity_range", lang, min=min_qty, max=max_qty)
            )
            return
        # Сохраняем количество наборов
        actual_cookies = quantity * set_size
    elif product_type == "topper":
        # Для топеров минимум 1 шт
        min_qty = settings.min_quantity_topper
        max_qty = 100
        if quantity < min_qty or quantity > max_qty:
            await message.answer(
                get_text("invalid_quantity_range", lang, min=min_qty, max=max_qty)
            )
            return
        actual_cookies = quantity
    elif product_type == "newyear":
        # Для новогодних пряников минимум 1 шт
        min_qty = 1
        max_qty = 100
        if quantity < min_qty or quantity > max_qty:
            await message.answer(
                get_text("invalid_quantity_range", lang, min=min_qty, max=max_qty)
            )
            return
        actual_cookies = quantity
    else:
        # Для остальных типов минимум 10 шт
        min_qty = settings.min_quantity
        max_qty = 100
        if quantity < min_qty or quantity > max_qty:
            await message.answer(
                get_text("invalid_quantity_min", lang, min=min_qty, max=max_qty)
            )
            return
        actual_cookies = quantity

    await state.update_data(quantity=quantity, actual_cookies=actual_cookies)

    # Рассчитываем примерную стоимость
    total_price = quantity * data["price_per_item"]
    await state.update_data(total_price=total_price)

    await state.set_state(OrderStates.entering_date)

    # Разные тексты для срочного и обычного заказа
    if data.get("is_urgent"):
        await message.answer(
            get_text("urgent_enter_date", lang, min_days=settings.min_preparation_days_urgent),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            get_text("enter_date", lang, min_days=settings.min_preparation_days),
            parse_mode="Markdown"
        )


@router.message(OrderStates.entering_date)
async def process_date(message: Message, state: FSMContext):
    """Обработка даты"""
    date_text = message.text.strip()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    try:
        delivery_date = parse_date(date_text)
    except ValueError:
        await message.answer(get_text("invalid_date", lang))
        return

    # Получаем данные о заказе
    is_urgent = data.get("is_urgent", False)

    # Проверяем что дата не в прошлом
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if delivery_date < today:
        await message.answer(get_text("date_in_past", lang))
        return

    # Проверяем минимальный срок (для срочных - 3 дня, для обычных - 10 дней)
    min_days = settings.min_preparation_days_urgent if is_urgent else settings.min_preparation_days
    min_date = datetime.now() + timedelta(days=min_days)
    if delivery_date < min_date:
        min_date_str = min_date.strftime("%d.%m.%Y")
        await message.answer(
            get_text("date_too_early", lang, min_days=min_days, min_date=min_date_str)
        )
        return

    # Проверяем доступность даты
    if not await check_date_availability(delivery_date):
        await message.answer(get_text("date_not_available", lang))
        return

    await state.update_data(
        delivery_date=delivery_date,
        date_formatted=delivery_date.strftime("%d.%m.%Y")
    )

    await state.set_state(OrderStates.entering_occasion)

    # Для тематических и срочных пряников показываем специальное сообщение с просьбой описать тему
    product_type = data.get("type")
    if product_type in ["themed", "urgent"]:
        await message.answer(get_text("enter_themed_description", lang), parse_mode="Markdown")
    else:
        await message.answer(get_text("enter_occasion", lang), parse_mode="Markdown")


@router.message(OrderStates.entering_occasion)
async def process_occasion(message: Message, state: FSMContext):
    """Обработка повода"""
    occasion = message.text.strip()
    data = await state.get_data()
    lang = data.get("lang", "ru")
    product_type = data.get("type")

    await state.update_data(occasion=occasion)

    # Для новогодних пряников запрашиваем комментарий
    if product_type == "newyear":
        await state.set_state(OrderStates.entering_comment)
        await message.answer(
            get_text("enter_newyear_comment", lang),
            parse_mode="Markdown"
        )
    else:
        await state.set_state(OrderStates.entering_phone)
        await message.answer(
            get_text("enter_phone", lang),
            reply_markup=phone_keyboard(lang),
            parse_mode="Markdown"
        )


@router.message(OrderStates.entering_comment)
async def process_comment(message: Message, state: FSMContext):
    """Обработка комментария для новогодних пряников"""
    comment = message.text.strip()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.update_data(comment=comment)

    await state.set_state(OrderStates.entering_phone)
    await message.answer(
        get_text("enter_phone", lang),
        reply_markup=phone_keyboard(lang),
        parse_mode="Markdown"
    )


@router.message(OrderStates.entering_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Обработка контакта с телефоном"""
    phone = message.contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone
    
    await state.update_data(phone=phone)
    await show_order_confirmation(message, state)


@router.message(OrderStates.entering_phone)
async def process_phone_text(message: Message, state: FSMContext):
    """Обработка телефона в виде текста"""
    phone = message.text.strip()
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if not validate_phone(phone):
        await message.answer(get_text("invalid_phone", lang))
        return

    await state.update_data(phone=phone)
    await show_order_confirmation(message, state)


async def show_order_confirmation(message: Message, state: FSMContext):
    """Показать подтверждение заказа"""
    data = await state.get_data()
    lang = data.get("lang", "ru")
    product_type = data.get("type")

    # Формируем текст подтверждения
    type_name = data.get("type_name", "")
    quantity = data.get("quantity", 0)
    date_formatted = data.get("date_formatted", "")
    occasion = data.get("occasion", "")
    phone = data.get("phone", "")
    total_price = data.get("total_price", 0.0)
    theme = data.get("theme", "")

    # Если есть тема, формируем строку темы (экранируем для Markdown)
    theme_line = ""
    if theme:
        safe_theme = escape_markdown(theme)
        theme_line = f"\n🎨 {get_text('theme_label', lang)}: {safe_theme}\n"

    # Для типов с подтипами показываем специальное подтверждение
    subtype_name = data.get("subtype_name")
    if subtype_name:
        price_per_item = data.get("price_per_item", 0.0)
        comment = data.get("comment", "")

        emoji_map = {"newyear": "🎄", "coloring": "🎨"}
        emoji = emoji_map.get(product_type, "📦")

        # Экранируем пользовательский ввод для Markdown
        safe_comment = escape_markdown(comment)
        safe_occasion = escape_markdown(occasion)
        safe_phone = escape_markdown(phone)

        confirmation_text = f"""{emoji} **{type_name}**
📋 Тип: {subtype_name} ({price_per_item} €)
📦 Кол-во: {quantity}"""

        if comment:
            confirmation_text += f"\n📋 Комментарий: {safe_comment}"

        confirmation_text += f"""
📅 Дата получения: {date_formatted}
🎉 Повод: {safe_occasion}
📱 Телефон: {safe_phone}

💰 **Итого: {total_price:.2f} EUR**"""
    else:
        # Экранируем пользовательский ввод для обычных заказов
        safe_occasion = escape_markdown(occasion)
        safe_phone = escape_markdown(phone)

        confirmation_text = get_text(
            "order_confirmation",
            lang,
            type=type_name,
            theme=theme_line,
            quantity=quantity,
            date=date_formatted,
            occasion=safe_occasion,
            phone=safe_phone,
            total=f"{total_price:.2f}"
        )

    await state.set_state(OrderStates.confirming_order)
    await message.answer(
        confirmation_text,
        reply_markup=confirmation_keyboard(lang),
        parse_mode="Markdown"
    )

    # Убираем клавиатуру с кнопкой "Отправить номер"
    await message.answer(
        get_text("check_order_above", lang),
        reply_markup=ReplyKeyboardRemove()
    )


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """Подтверждение заказа"""
    # Проверяем что мы в правильном состоянии
    current_state = await state.get_state()
    if current_state != OrderStates.confirming_order.state:
        await callback.answer("❌ Ошибка: неверное состояние")
        return
    data = await state.get_data()
    
    # Получаем клиента
    customer = await get_customer_by_telegram_id(callback.from_user.id)
    
    # Для типов с подтипами сохраняем подтип в theme_description, а комментарий в notes
    product_type = data["type"]
    subtype_name = data.get("subtype_name")
    if subtype_name:
        theme_desc = subtype_name
        notes = data.get("comment", "")
    else:
        theme_desc = data.get("theme", "")
        notes = ""

    # Создаем заказ
    order = await create_order(
        customer_id=customer.id,
        product_type=product_type,
        theme_description=theme_desc,
        quantity=data["quantity"],
        price_per_item=data["price_per_item"],
        total_price=data["total_price"],
        delivery_date=data["delivery_date"],
        occasion=data["occasion"],
        notes=notes,
        phone=data["phone"],
        telegram_message_id=callback.message.message_id
    )

    # Инвалидируем кэш заказов клиента после создания нового заказа
    order_cache.invalidate(customer.id)

    # Получаем язык клиента
    lang = data.get("lang", "ru")

    # Отправляем подтверждение клиенту о получении заказа
    confirmation_text = get_text(
        "order_accepted",
        lang,
        order_number=order.order_number,
        date=data['date_formatted'],
        total=f"{data['total_price']:.2f}"
    )

    await callback.message.edit_text(
        confirmation_text,
        parse_mode="Markdown"
    )
    
    # Добавляем событие в Google Calendar
    if settings.google_calendar_enabled:
        try:
            from bot.utils.google_calendar import calendar_integration

            event_id = calendar_integration.create_order_event(
                order_number=order.order_number,
                customer_name=customer.name or 'Не указано',
                product_type=data['type_name'],
                quantity=data['quantity'],
                delivery_date=data['delivery_date'],
                phone=data['phone'],
                occasion=data['occasion'],
                preparation_days=settings.min_preparation_days
            )

            if event_id:
                print(f"✅ Заказ добавлен в Google Calendar: {event_id}")
            else:
                print("⚠️ Не удалось добавить заказ в Google Calendar")
        except Exception as e:
            print(f"Ошибка добавления в Google Calendar: {e}")

    # Уведомляем всех админов о новом заказе
    urgent_marker = "🚨 **СРОЧНЫЙ ЗАКАЗ**\n\n" if data.get('is_urgent') else ""
    admin_text = f"""🔔 **Новый заказ #{order.order_number}**

{urgent_marker}👤 Клиент: {customer.name or 'Не указано'}
📱 Телефон: {data['phone']}
🍪 Тип: {data['type_name']}
{f"🎨 Тема: {data.get('theme', '')}" if data.get('theme') else ""}
📦 Количество: {data['quantity']} шт
📅 Дата: {data['date_formatted']}
🎉 Повод: {data['occasion']}
💰 Сумма: {data['total_price']}€

⏳ **Ожидает подтверждения**"""

    # Создаем кнопки для подтверждения/отклонения
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    approval_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"approve_order_{order.order_number}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_order_{order.order_number}")
        ]
    ])

    try:
        from bot.main import bot
        for admin_id in settings.admin_ids_list:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_text,
                    reply_markup=approval_keyboard,
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Ошибка отправки уведомления админу {admin_id}: {e}")
    except Exception as e:
        print(f"Ошибка отправки уведомлений админам: {e}")

    await state.clear()
    await callback.answer("Заказ принят! 🎉")


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext, **kwargs):
    """Отмена заказа"""
    await state.clear()

    lang = get_user_lang(kwargs)

    await callback.message.edit_text(
        get_text("order_cancelled", lang),
        reply_markup=main_menu(lang, callback.from_user.id)
    )
    await callback.answer()