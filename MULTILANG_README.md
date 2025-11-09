# Мультиязычность бота

Бот поддерживает 3 языка:
- 🇷🇺 Русский (ru) - по умолчанию
- 🇬🇧 English (en)
- 🇺🇦 Українська (uk)

## Как это работает

1. При первом запуске `/start` бот предлагает выбрать язык
2. Выбор сохраняется в поле `language` таблицы `customers`
3. Все тексты хранятся в `bot/utils/translations.py`
4. Функция `get_text(key, lang, **kwargs)` возвращает текст на нужном языке
5. Пользователь может изменить язык через кнопку "🌐 Изменить язык" в главном меню

## Для разработчиков

### Добавление нового текста

1. Откройте `bot/utils/translations.py`
2. Добавьте новый ключ в словарь `TRANSLATIONS`:

```python
"new_text_key": {
    "ru": "Текст на русском",
    "en": "Text in English",
    "uk": "Текст українською"
}
```

### Использование в коде

```python
from bot.utils.translations import get_text
from database.crud import get_customer_language

# Получаем язык пользователя
lang = await get_customer_language(user_id)

# Получаем текст
text = get_text("welcome", lang, master_name="Любовь")
```

### Админские сообщения

Все сообщения для администраторов остаются на русском языке.

## База данных

Поле `language` добавлено в таблицу `customers`:
- Тип: String(2)
- По умолчанию: "ru"
- Возможные значения: "ru", "en", "uk"

## CRUD функции

- `get_customer_language(telegram_user_id)` - получить язык пользователя
- `update_customer_language(telegram_user_id, language)` - обновить язык

