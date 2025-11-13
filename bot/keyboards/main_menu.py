from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config.settings import GINGERBREAD_TYPES, POPULAR_THEMES, POPULAR_THEMES_TRANSLATIONS, settings
from bot.utils.translations import get_text


def main_menu(lang: str = "ru", user_id: int = None) -> InlineKeyboardMarkup:
    """Главное меню"""
    buttons = [
        [InlineKeyboardButton(text=get_text("btn_view_and_order", lang), callback_data="view_and_order")],
        [InlineKeyboardButton(text=get_text("btn_contacts", lang), callback_data="contacts")],
    ]

    # Добавляем кнопку админ-панели только для администраторов
    if user_id and settings.is_admin(user_id):
        admin_text = {"ru": "🔧 Админ панель", "en": "🔧 Admin panel", "uk": "🔧 Адмін панель"}
        buttons.append([InlineKeyboardButton(text=admin_text.get(lang, admin_text["ru"]), callback_data="admin_panel")])

    buttons.append([InlineKeyboardButton(text=get_text("btn_change_language", lang), callback_data="change_language")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def gingerbread_types(lang: str = "ru") -> InlineKeyboardMarkup:
    """Выбор типа пряников"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for type_key, type_data in GINGERBREAD_TYPES.items():
        type_name = get_text(f"type_{type_key}", lang)
        price_from = get_text("price_from", lang)
        button_text = f"{type_data['emoji']} {type_name} - {price_from} {type_data['price']}€"
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=button_text, callback_data=f"type_{type_key}")
        ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_menu")
    ])

    return keyboard


def popular_themes(lang: str = "ru") -> InlineKeyboardMarkup:
    """Популярные темы для тематических пряников"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    # Получаем список тем в нужном языке
    theme_keys = list(POPULAR_THEMES_TRANSLATIONS.keys())

    # По 2 темы в ряд
    for i in range(0, len(theme_keys), 2):
        row = []
        for j in range(2):
            if i + j < len(theme_keys):
                theme_key = theme_keys[i + j]
                theme_name = POPULAR_THEMES_TRANSLATIONS[theme_key].get(lang, POPULAR_THEMES_TRANSLATIONS[theme_key]["ru"])
                row.append(InlineKeyboardButton(
                    text=theme_name,
                    callback_data=f"theme_{theme_key}"
                ))
        keyboard.inline_keyboard.append(row)

    # Кнопка "Своя тема"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=get_text("btn_custom_theme", lang), callback_data="custom_theme")
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_types")
    ])

    return keyboard


def confirmation_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Подтверждение заказа"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_confirm", lang), callback_data="confirm_order"),
            InlineKeyboardButton(text=get_text("btn_cancel", lang), callback_data="cancel_order")
        ]
    ])
    return keyboard


def phone_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура для отправки номера телефона"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text("btn_send_phone", lang), request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def contacts_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура контактов с кнопками связи"""
    from config.settings import settings

    buttons = []

    # Кнопка локации (если есть координаты)
    if settings.pickup_coordinates:
        coords = settings.pickup_coordinates.split(',')
        if len(coords) == 2:
            buttons.append([InlineKeyboardButton(
                text="📍 Показать на карте" if lang == "ru" else ("📍 Show on map" if lang == "en" else "📍 Показати на карті"),
                url=f"https://maps.google.com/?q={coords[0]},{coords[1]}"
            )])

    # Кнопка назад
    buttons.append([InlineKeyboardButton(text=get_text("btn_main_menu", lang), callback_data="back_to_menu")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def admin_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Админское меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_admin_orders", lang), callback_data="admin_orders")],
        [InlineKeyboardButton(text=get_text("btn_admin_calendar", lang), callback_data="admin_calendar")],
        [InlineKeyboardButton(text=get_text("btn_admin_stats", lang), callback_data="admin_stats")],
        [InlineKeyboardButton(text=get_text("btn_admin_broadcast", lang), callback_data="admin_broadcast")]
    ])
    return keyboard