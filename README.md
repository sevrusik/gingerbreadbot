# 🍪 Gingerbread Bot - Бот для заказа пряников

Telegram-бот для автоматизации приема заказов на изготовление расписных пряников.

## 🌟 Особенности

- **Персональное общение** - бот представляется как мастер Любовь
- **Простой процесс заказа** - всего несколько шагов до готового заказа
- **Визуальные примеры** - клиенты видят фото каждого типа пряников при выборе
- **Гибкая типизация** - классические, раскраски, цифры, тематические пряники
- **Умная валидация** - проверка дат, телефонов, доступности
- **Админ-панель** - управление заказами, статистика, календарь
- **Уведомления** - автоматические напоминания клиентам и админу

## 🚀 Быстрый старт

### 1. Клонирование и настройка

```bash
# Клонирование репозитория
git clone <repository-url>
cd gingerbread-bot

# Автоматическая настройка
./scripts/setup.sh
```

### 2. Настройка бота

Отредактируйте файл `.env`:

```bash
# Основные настройки
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz  # От @BotFather
ADMIN_USER_ID=123456789                                   # Ваш Telegram ID

# Бизнес настройки
MASTER_NAME=Любовь
BUSINESS_PHONE=+7-xxx-xxx-xx-xx
PICKUP_ADDRESS=ул. Мастеров, 12
WORKING_HOURS=10:00-12:00, 18:00-20:00

# Цены
BASE_PRICE_EUR=2.0
COLORING_PRICE_EUR=3.5
```

### 3. Получение Telegram Bot Token

1. Напишите [@BotFather](https://t.me/botfather)
2. Выполните команду `/newbot`
3. Придумайте имя и username для бота
4. Скопируйте полученный токен в `.env`

### 4. Получение вашего Telegram ID

1. Напишите [@userinfobot](https://t.me/userinfobot)
2. Скопируйте ваш ID в `.env` как `ADMIN_USER_ID`

### 5. Добавление изображений-примеров (опционально)

Для улучшения пользовательского опыта добавьте фотографии ваших пряников:

```bash
# Разместите изображения в папке media/examples/
# Поддерживаемые форматы: .jpg, .jpeg, .png, .webp
# Названия файлов должны соответствовать типам:
media/examples/
├── classic.jpg    # Классические расписные пряники
├── coloring.jpg   # Пряники-раскраски с красками
├── numbers.jpg    # Пряники в виде цифр
├── themed.jpg     # Тематические пряники
└── urgent.jpg     # Пример для срочного заказа
```

**Рекомендации по изображениям:**
- Размер: 800-1200px по длинной стороне
- Формат: JPG (оптимальное сжатие)
- Качество: хорошее освещение, нейтральный фон
- Содержание: несколько пряников соответствующего типа

Если изображения не добавлены, бот будет работать без них - клавиатура выбора будет отображаться без фото-примеров.

### 6. Запуск бота

```bash
# Через скрипт (рекомендуется)
./scripts/start.sh

# Или напрямую
python run.py
```

## 📋 Типы пряников

| Тип | Описание | Цена | Комплектация |
|-----|----------|------|--------------|
| **Классические** | Готовые расписные | 2€/шт | Пряник с глазурью |
| **Раскраски** | Для творчества | 3.5€/шт | Пряник + краски + кисточка + упаковка |
| **Цифры** | Для дней рождения | 2€/шт | Пряник в виде цифры |
| **Тематические** | Индивидуальный дизайн | от 2€/шт | По заказу |

## 🎯 Процесс заказа

1. **Выбор типа** - классические, раскраски, цифры, тематические
2. **Тема/дизайн** - для тематических пряников
3. **Количество** - от 1 до 100 штук
4. **Дата готовности** - минимум 3 дня
5. **Повод** - описание события
6. **Контакт** - номер телефона
7. **Подтверждение** - итоговый заказ

## 👨‍💼 Админские команды

### Команды в чате
- `/admin` - админская панель
- `/today` - заказы на сегодня
- `/tomorrow` - заказы на завтра
- `/status <номер> <статус>` - изменить статус заказа

### Статусы заказов
- `new` - новый заказ
- `confirmed` - подтвержден
- `in_progress` - в работе
- `ready` - готов к выдаче
- `completed` - выполнен
- `cancelled` - отменен

### Панель управления
- 📋 **Активные заказы** - список текущих заказов
- 📅 **Календарь** - заказы по дням
- 📊 **Статистика** - выручка и аналитика

## 🗄️ Структура базы данных

### Customers (Клиенты)
- `telegram_user_id` - ID в Telegram
- `phone` - номер телефона
- `name` - имя клиента

### Orders (Заказы)
- `order_number` - уникальный номер
- `product_type` - тип пряников
- `quantity` - количество
- `delivery_date` - дата готовности
- `status` - статус заказа
- `total_price` - общая стоимость

### Calendar (Календарь)
- `date` - дата
- `available_slots` - доступные слоты
- `booked_orders` - забронированные заказы

## 🔧 Технические детали

### Стек технологий
- **Python 3.8+** - основной язык
- **aiogram 3.4** - Telegram Bot API
- **SQLAlchemy** - ORM для базы данных
- **SQLite/PostgreSQL** - база данных
- **asyncio** - асинхронность

### Системные требования
- **Python** 3.8 или выше
- **RAM** минимум 512MB
- **Диск** 1GB свободного места
- **Интернет** стабильное соединение

### Для MacMini M4
```bash
# Установка через Homebrew
brew install python@3.11 postgresql

# Запуск PostgreSQL (опционально)
brew services start postgresql
```

## 🔐 Безопасность

- Токен бота хранится в `.env` файле (не попадает в Git)
- Проверка прав администратора для всех admin команд
- Валидация всех пользовательских данных
- Логирование всех операций
- Резервное копирование базы данных

## 📂 Структура проекта

```
gingerbread-bot/
├── .env                    # Конфигурация (создается автоматически)
├── .gitignore             # Исключения Git
├── requirements.txt       # Python зависимости
├── README.md             # Документация
├── run.py                # Точка входа
├── config/
│   ├── settings.py       # Настройки приложения
│   └── database.py       # Конфигурация БД
├── bot/
│   ├── main.py           # Основной файл бота
│   ├── handlers/         # Обработчики команд
│   │   ├── start.py      # Команда /start и навигация
│   │   ├── order.py      # Процесс заказа
│   │   └── admin.py      # Админские команды
│   ├── keyboards/        # Клавиатуры
│   │   └── main_menu.py  # Основные клавиатуры
│   ├── states/           # FSM состояния
│   │   └── order_states.py
│   └── utils/            # Утилиты
│       ├── texts.py      # Тексты сообщений
│       ├── validators.py # Валидация данных
│       └── media_helper.py # Работа с изображениями
├── database/
│   ├── models.py         # Модели SQLAlchemy
│   ├── crud.py           # CRUD операции
│   └── orders.db         # База SQLite (создается автоматически)
├── media/
│   └── examples/         # Изображения-примеры типов пряников
│       ├── classic.jpg   # Классические расписные
│       ├── coloring.jpg  # Пряники-раскраски
│       ├── numbers.jpg   # Цифры
│       ├── themed.jpg    # Тематические
│       └── urgent.jpg    # Пример для срочного заказа
├── logs/                 # Логи приложения
├── backups/              # Резервные копии
└── scripts/              # Скрипты управления
    ├── setup.sh          # Первоначальная настройка
    ├── start.sh          # Запуск бота
    └── backup.sh         # Резервное копирование
```

## 🚀 Развертывание на MacMini M4

### Подготовка системы

```bash
# Установка зависимостей через Homebrew
brew install python@3.11 git

# Создание пользователя для бота (опционально)
sudo dscl . -create /Users/gingerbot
sudo dscl . -create /Users/gingerbot UserShell /bin/bash
sudo dscl . -create /Users/gingerbot RealName "Gingerbread Bot"
```

### Автозапуск (через launchd)

Создайте файл `~/Library/LaunchAgents/com.gingerbot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.gingerbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/gingerbread-bot/scripts/start.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/gingerbread-bot</string>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/gingerbread-bot/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/gingerbread-bot/logs/launchd.error.log</string>
</dict>
</plist>
```

Загрузите сервис:
```bash
launchctl load ~/Library/LaunchAgents/com.gingerbot.plist
launchctl start com.gingerbot
```

## 📊 Мониторинг и обслуживание

### Логи
```bash
# Просмотр логов в реальном времени
tail -f logs/bot_*.log

# Архивация старых логов
find logs/ -name "*.log" -mtime +30 -delete
```

### Резервное копирование
```bash
# Ручное создание бэкапа
./scripts/backup.sh

# Автоматическое (добавить в crontab)
0 2 * * * /path/to/gingerbread-bot/scripts/backup.sh
```

### Статистика использования
```bash
# Размер базы данных
du -h database/orders.db

# Количество заказов
sqlite3 database/orders.db "SELECT COUNT(*) FROM orders;"

# Выручка за месяц
sqlite3 database/orders.db "SELECT SUM(total_price) FROM orders WHERE created_at > date('now', '-1 month');"
```

## 🛠️ Настройка сети

### DDNS для MacMini

1. **Регистрация на DuckDNS**:
   - Перейдите на [duckdns.org](https://www.duckdns.org)
   - Зарегистрируйтесь и создайте домен: `yourbot.duckdns.org`

2. **Автообновление IP**:
```bash
# Создайте скрипт ~/scripts/update-ddns.sh
#!/bin/bash
curl "https://www.duckdns.org/update?domains=yourbot&token=YOUR_TOKEN&ip="

# Добавьте в crontab (каждые 5 минут)
*/5 * * * * /Users/youruser/scripts/update-ddns.sh
```

### Настройка роутера

1. **Проброс портов**:
   - 443 → MacMini:443 (HTTPS webhook)
   - 8080 → MacMini:8080 (веб-админка, опционально)

2. **Статический IP для MacMini**:
   - Настройте резервирование DHCP
   - Или настройте статический IP в macOS

### SSL сертификат

```bash
# Установка certbot
brew install certbot

# Получение сертификата
sudo certbot certonly --standalone -d yourbot.duckdns.org

# Автообновление сертификата
0 0 1 * * sudo certbot renew --quiet
```

## 🔧 Настройка webhook (для продакшена)

По умолчанию бот работает через polling, но для продакшена рекомендуется webhook:

```bash
# В .env добавьте:
WEBHOOK_URL=https://yourbot.duckdns.org
WEBHOOK_PATH=/webhook
```

## 📱 Уведомления и интеграции

### Push-уведомления на телефон

Интегрируйте с Pushover или Telegram для уведомлений:

```python
# В admin.py добавьте отправку уведомлений
async def send_push_notification(message: str):
    # Отправка через Pushover API или другой сервис
    pass
```

### Интеграция с календарем

```python
# Синхронизация с iCal/Google Calendar
async def sync_with_calendar():
    # Экспорт заказов в календарь
    pass
```

## 🐛 Устранение неполадок

### Частые проблемы

1. **Бот не отвечает**:
   ```bash
   # Проверьте логи
   tail -f logs/bot_*.log
   
   # Проверьте процесс
   ps aux | grep python
   ```

2. **Ошибки базы данных**:
   ```bash
   # Проверьте целостность SQLite
   sqlite3 database/orders.db "PRAGMA integrity_check;"
   
   # Восстановление из бэкапа
   cp backups/orders_YYYYMMDD.db database/orders.db
   ```

3. **Проблемы с webhook**:
   ```bash
   # Проверьте сертификат
   openssl s_client -connect yourbot.duckdns.org:443
   
   # Тест webhook
   curl -X POST https://yourbot.duckdns.org/webhook
   ```

### Отладка

```bash
# Запуск в режиме отладки
DEBUG=True python run.py

# Подробные логи
LOG_LEVEL=DEBUG python run.py
```

## 📈 Масштабирование

### При росте нагрузки

1. **Переход на PostgreSQL**:
   ```bash
   # Установка PostgreSQL
   brew install postgresql
   brew services start postgresql
   
   # Создание базы
   createdb gingerbread_bot
   
   # В .env:
   DATABASE_URL=postgresql://user:password@localhost/gingerbread_bot
   ```

2. **Использование Redis для кеширования**:
   ```bash
   brew install redis
   brew services start redis
   ```

3. **Перенос на VPS**:
   - При >100 заказов в день
   - Или при нестабильном домашнем интернете

## 🤝 Поддержка и разработка

### Добавление новых функций

1. Создайте новый обработчик в `bot/handlers/`
2. Зарегистрируйте в `bot/main.py`
3. Добавьте тесты (если необходимо)

### Структура коммитов

```
feat: добавить новый тип пряников
fix: исправить валидацию телефона
docs: обновить README
refactor: оптимизировать запросы к БД
```

## 📞 Контакты

При возникновении вопросов или проблем:
- Создайте Issue в репозитории
- Проверьте логи бота
- Обратитесь к документации

---

**Приятной работы с ботом! 🍪✨**