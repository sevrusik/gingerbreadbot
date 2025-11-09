# 🚀 Деплой на Render

Это руководство покажет, как развернуть Gingerbread Bot на платформе [Render](https://render.com).

## ✨ Преимущества Render

- ✅ **Бесплатный тариф** - до 750 часов в месяц
- ✅ **Автоматический деплой** из GitHub
- ✅ **Бесплатная PostgreSQL** база данных
- ✅ **SSL сертификаты** автоматически
- ✅ **Логи и мониторинг** встроены

## 📋 Подготовка

### 1. Создайте аккаунт на Render

Зарегистрируйтесь на [render.com](https://render.com) и свяжите с GitHub.

### 2. Получите Telegram Bot Token

1. Напишите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям
4. Сохраните полученный токен (например: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Получите ваш Telegram User ID

1. Напишите боту [@userinfobot](https://t.me/userinfobot)
2. Он отправит вам ваш ID (например: `123456789`)
3. Сохраните этот ID - он понадобится для админ-панели

## 🎯 Деплой через Blueprint (Рекомендуется)

### Вариант 1: Автоматический деплой (самый простой)

1. **Нажмите на кнопку Deploy to Render:**

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sevrusik/gingerbreadbot)

2. **Заполните переменные окружения:**
   - `TELEGRAM_BOT_TOKEN` - токен от BotFather
   - `ADMIN_USER_IDS` - ваш Telegram ID

3. **Нажмите "Apply" и дождитесь деплоя**

### Вариант 2: Ручная настройка через Blueprint

1. **Создайте новый Blueprint:**
   - Зайдите в [Render Dashboard](https://dashboard.render.com)
   - Нажмите "New +" → "Blueprint"
   - Подключите ваш GitHub репозиторий
   - Render автоматически найдет `render.yaml`

2. **Настройте переменные:**
   - `TELEGRAM_BOT_TOKEN` - ваш токен от BotFather
   - `ADMIN_USER_IDS` - ваш Telegram User ID
   - Остальные переменные уже настроены в `render.yaml`

3. **Нажмите "Apply" и дождитесь деплоя**

## 🔧 Ручной деплой (альтернатива)

Если Blueprint не работает, можно настроить вручную:

### Шаг 1: Создайте PostgreSQL базу данных

1. В [Render Dashboard](https://dashboard.render.com) нажмите "New +" → "PostgreSQL"
2. Заполните:
   - **Name:** `gingerbread-db`
   - **Database:** `gingerbread_bot`
   - **User:** `gingerbread_user`
   - **Region:** Frankfurt (или ближайший)
   - **Plan:** Free
3. Нажмите "Create Database"
4. Сохраните **Internal Database URL** (понадобится позже)

### Шаг 2: Создайте Web Service

1. Нажмите "New +" → "Web Service"
2. Выберите "Build and deploy from a Git repository"
3. Подключите ваш GitHub репозиторий `gingerbreadbot`
4. Заполните:
   - **Name:** `gingerbread-bot`
   - **Region:** Frankfurt
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Plan:** Free

### Шаг 3: Настройте переменные окружения

В разделе "Environment Variables" добавьте:

#### Обязательные:
```
TELEGRAM_BOT_TOKEN = ваш_токен_от_BotFather
ADMIN_USER_IDS = ваш_telegram_id
DATABASE_URL = [скопируйте Internal Database URL из Step 1]
```

#### Бизнес-настройки:
```
MASTER_NAME = Liubov
BUSINESS_PHONE = +357-95-161-375
PICKUP_ADDRESS = Larnaka,Thessalonikiss 13
PICKUP_COORDINATES = 34.9161781,33.6202820
WORKING_HOURS = 09:00-18:00
```

#### Цены и лимиты:
```
BASE_PRICE_EUR = 2.0
COLORING_PRICE_EUR = 12.0
TOPPER_PRICE_EUR = 5.0
RUSH_ORDER_MULTIPLIER = 2
MIN_PREPARATION_DAYS = 10
MIN_PREPARATION_DAYS_URGENT = 3
MIN_QUANTITY = 10
MIN_QUANTITY_TOPPER = 1
COLORING_SET_SIZE = 3
```

#### Опциональные:
```
DEBUG = False
LOG_LEVEL = INFO
GOOGLE_CALENDAR_ENABLED = False
```

### Шаг 4: Деплой

1. Нажмите "Create Web Service"
2. Render начнет сборку и деплой
3. Дождитесь завершения (обычно 2-5 минут)

## ✅ Проверка работы

1. **Откройте логи** в Render Dashboard
2. Вы должны увидеть:
   ```
   🍪 Запуск бота для заказа пряников...
   Начинаем polling...
   Start polling
   ```
3. **Напишите боту** в Telegram команду `/start`
4. Бот должен ответить приветственным сообщением

## 🔄 Автоматические обновления

После настройки каждый `git push` в ветку `main` будет автоматически деплоить новую версию на Render.

## 📊 Мониторинг

### Логи
- Зайдите в ваш Web Service на Render
- Откройте вкладку "Logs"
- Здесь вы увидите все логи бота в реальном времени

### База данных
- Откройте вашу PostgreSQL базу на Render
- Во вкладке "Metrics" можно посмотреть использование
- Во вкладке "Shell" можно выполнить SQL запросы

### Статистика заказов
В боте напишите `/admin` → "📊 Статистика"

## ⚠️ Важные замечания

### Лимиты бесплатного тариа Render:

1. **Web Service:**
   - Засыпает после 15 минут неактивности
   - Просыпается при первом запросе (холодный старт ~30 сек)
   - 750 часов в месяц (достаточно для одного бота)

2. **PostgreSQL:**
   - 1 GB хранилища
   - Хватит на ~50,000 заказов
   - Автоматический бэкап не включен на Free плане

3. **Решение проблемы засыпания:**
   - Используйте [UptimeRobot](https://uptimerobot.com) для пинга каждые 5 минут
   - Или перейдите на платный тариф ($7/месяц)

### Бэкап базы данных

На Free плане автоматический бэкап отключен. Рекомендуется:

1. Настроить периодический экспорт через cron
2. Или использовать платный план Render ($7/месяц)
3. Или вручную делать бэкапы через Render Shell

## 🆘 Проблемы и решения

### Бот не отвечает
1. Проверьте логи на Render
2. Убедитесь что все переменные окружения заполнены
3. Проверьте что токен бота правильный

### Ошибка подключения к базе
1. Убедитесь что `DATABASE_URL` правильный
2. Проверьте что PostgreSQL база создана
3. Попробуйте пересоздать подключение

### Бот засыпает
1. Это нормально для Free плана
2. Используйте UptimeRobot для постоянной работы
3. Или перейдите на платный план

## 📚 Дополнительные ресурсы

- [Render Docs](https://render.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Aiogram Documentation](https://docs.aiogram.dev/)

## 💬 Поддержка

Если возникли проблемы:
1. Проверьте логи на Render
2. Изучите [Issues на GitHub](https://github.com/sevrusik/gingerbreadbot/issues)
3. Создайте новый Issue с описанием проблемы
