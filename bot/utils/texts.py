from config.settings import settings, GINGERBREAD_TYPES

class BotTexts:
    # Приветствие
    WELCOME = f"""Здравствуйте! Меня зовут {settings.master_name} 😊

Я изготавливаю вкусные расписные пряники для любых событий:
🎂 Дни рождения и праздники
🏫 Детские садики и школы  
🎁 Подарочные наборы
✨ Особые торжества

Что вас интересует?"""

    # Типы пряников
    CHOOSE_TYPE = """Выберите тип пряников:

🍪 **Классические расписные** - {classic_price}€/шт
Готовые пряники с красивой глазурью

🎨 **Пряники-раскраски** - от {coloring_price}€/набор
С красками и кисточкой в комплекте

🔢 **Цифры** - {numbers_price}€/шт
Для дней рождения

✨ **Тематические** - от {themed_price}€/шт
По индивидуальному дизайну""".format(
        classic_price=GINGERBREAD_TYPES["classic"]["price"],
        coloring_price=settings.coloring_price_eur,  # Используем минимальную цену из настроек
        numbers_price=GINGERBREAD_TYPES["numbers"]["price"],
        themed_price=GINGERBREAD_TYPES["themed"]["price"]
    )

    # Темы
    CHOOSE_THEME = """Отличный выбор! ✨

Какая тематика вас интересует?
Можете выбрать из популярных или написать свою идею:"""

    CUSTOM_THEME = "Напишите свою тему или описание дизайна:"

    # Количество
    ENTER_QUANTITY = """Сколько пряников нужно?

Напишите число (например: 15)"""

    # Дата
    ENTER_DATE = f"""На какую дату нужны пряники?

Напишите дату в формате ДД.ММ или ДД.ММ.ГГГГ
Например: 25.07 или 25.07.2024

⏰ Минимальный срок изготовления: {settings.min_preparation_days} дня"""

    # Повод
    ENTER_OCCASION = """Расскажите о поводе заказа:

Например:
• День рождения дочки (5 лет)
• Для детского садика
• Корпоративное мероприятие
• Подарок коллегам

Эта информация поможет лучше подготовить дизайн 😊"""

    # Телефон
    ENTER_PHONE = """Укажите ваш номер телефона для связи:

Можете написать или отправить контакт через кнопку ниже 📱"""

    # Подтверждение заказа
    def order_confirmation(self, order_data: dict) -> str:
        urgent_text = "🚨 **СРОЧНЫЙ ЗАКАЗ** (двойная стоимость)\n\n" if order_data.get('is_urgent') else ""
        return f"""📋 **Подтверждение заказа**

{urgent_text}{GINGERBREAD_TYPES[order_data['type']]['emoji']} **Тип:** {GINGERBREAD_TYPES[order_data['type']]['name']}
{f"🎨 **Тема:** {order_data['theme']}" if order_data.get('theme') else ""}
📦 **Количество:** {order_data['quantity']} шт
📅 **Дата готовности:** {order_data['date_formatted']}
🎉 **Повод:** {order_data['occasion']}
💰 **Стоимость:** {order_data['total_price']}€

📞 **Ваш телефон:** {order_data['phone']}

Все верно?"""

    ORDER_CONFIRMED = """✅ **Заказ принят!**

**Номер заказа:** #{order_number}

📍 **Самовывоз:**
{pickup_address}
🕐 **Время работы:** {working_hours}

💰 **Оплата:** наличными при получении

За день до готовности пришлю напоминание и фото готовых пряников 📸

Спасибо за заказ! 💛""".format(
        order_number="{order_number}",
        pickup_address=settings.pickup_address,
        working_hours=settings.working_hours
    )

    # Ошибки
    INVALID_QUANTITY = "Пожалуйста, введите корректное количество (число от 1 до 100)"
    INVALID_DATE = "Некорректная дата. Используйте формат ДД.ММ или ДД.ММ.ГГГГ"
    DATE_TOO_EARLY = f"Дата слишком близкая. Минимальный срок: {settings.min_preparation_days} дня"
    DATE_NOT_AVAILABLE = "К сожалению, эта дата уже занята. Выберите другую дату"
    INVALID_PHONE = "Пожалуйста, введите корректный номер телефона"

    # Кнопки
    BTN_ORDER = "🛒 Сделать заказ"
    BTN_CATALOG = "📋 Каталог пряников"
    BTN_CONTACT = "📞 Контакты"
    BTN_BACK = "⬅️ Назад"
    BTN_CONFIRM = "✅ Подтвердить"
    BTN_CANCEL = "❌ Отменить"
    BTN_SEND_PHONE = "📱 Отправить номер"
    BTN_CUSTOM_THEME = "✏️ Своя тема"

    # Контакты
    CONTACTS = f"""📞 **Контактная информация**

👤 **Мастер:** {settings.master_name}
📱 **Телефон:** {settings.business_phone}

📍 **Адрес самовывоза:**
{settings.pickup_address}

🕐 **Время работы:**
{settings.working_hours}

💰 **Оплата:** наличными при получении
⏰ **Срок изготовления:** от {settings.min_preparation_days} дней"""