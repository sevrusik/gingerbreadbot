# Развертывание на Synology NAS 218+

## Способ 1: Docker Compose через SSH (Рекомендуется)

### Преимущества
- Автоматическая загрузка переменных из `.env`
- Проще обновлять и перезапускать
- Меньше ошибок конфигурации

### Инструкция

1. **Включите SSH на Synology**
   - Control Panel → Terminal & SNMP
   - Включите SSH service (порт 22)

2. **Подключитесь по SSH**
   ```bash
   ssh your_username@synology_ip
   ```

3. **Перейдите в папку проекта**
   ```bash
   cd /volume1/docker/gingerbread-bot
   ```

4. **Убедитесь что .env файл существует**
   ```bash
   ls -la .env
   cat .env | grep TELEGRAM_BOT_TOKEN
   ```

5. **Остановите контейнеры (если запущены через UI)**
   - Откройте Container Manager
   - Остановите и удалите контейнеры `gingerbread-bot` и `gingerbread-db`

6. **Запустите через docker-compose**
   ```bash
   sudo docker-compose up -d
   ```

7. **Проверьте статус**
   ```bash
   sudo docker-compose ps
   sudo docker-compose logs -f bot
   ```

8. **Автозапуск после перезагрузки**
   Docker Compose автоматически перезапустит контейнеры благодаря `restart: always` в конфигурации.

### Полезные команды

```bash
# Просмотр логов
sudo docker-compose logs -f bot

# Перезапуск бота
sudo docker-compose restart bot

# Остановка всех сервисов
sudo docker-compose down

# Пересборка и перезапуск
sudo docker-compose up -d --build

# Просмотр переменных окружения в контейнере
sudo docker-compose exec bot env | grep TELEGRAM
```

---

## Способ 2: Container Manager UI (Если SSH недоступен)

### Шаг 1: Подготовка образа

1. **Откройте Container Manager** → Image → Add → Add from File
2. **Создайте образ из Dockerfile**:
   - Загрузите папку проекта на NAS
   - Используйте терминал DSM для сборки:
     ```bash
     cd /volume1/docker/gingerbread-bot
     sudo docker build -t gingerbread-bot:latest .
     ```

### Шаг 2: Создание контейнера PostgreSQL

1. **Container Manager → Container → Create**
2. **Образ**: `postgres:15-alpine`
3. **Имя контейнера**: `gingerbread-db`
4. **Network**: Создайте новую сеть `gingerbread-network` (Container Manager → Network → Create)
5. **Переменные окружения**:
   ```
   POSTGRES_USER=gingerbread_user
   POSTGRES_PASSWORD=changeme123
   POSTGRES_DB=gingerbread_bot
   ```
6. **Volume Mappings**:
   - File/Folder: `/volume1/docker/gingerbread-bot/data/postgres`
   - Mount path: `/var/lib/postgresql/data`
7. **Auto-restart**: Enable
8. **Применить** и запустить

### Шаг 3: Создание контейнера бота

1. **Container Manager → Container → Create**
2. **Образ**: `gingerbread-bot:latest`
3. **Имя контейнера**: `gingerbread-bot`
4. **Network**: `gingerbread-network`
5. **Links**: Добавить `gingerbread-db`

6. **Переменные окружения** (важно!):
   ```
   TELEGRAM_BOT_TOKEN=8313090422:AAFQIjNFVRHRIgnY4JRTN3CUXgA5r8mSvlI
   ADMIN_USER_IDS=ваш_telegram_user_id
   DATABASE_URL=postgresql+asyncpg://gingerbread_user:changeme123@gingerbread-db:5432/gingerbread_bot
   LOG_LEVEL=INFO
   MASTER_NAME=Любовь
   BASE_PRICE_EUR=2.0
   COLORING_PRICE_EUR=12.0
   TOPPER_PRICE_EUR=5.0
   MIN_PREPARATION_DAYS=10
   MIN_PREPARATION_DAYS_URGENT=3
   MIN_QUANTITY=10
   MIN_QUANTITY_TOPPER=1
   COLORING_SET_SIZE=3
   ```

7. **Volume Mappings**:
   - `/volume1/docker/gingerbread-bot/logs` → `/app/logs`
   - `/volume1/docker/gingerbread-bot/media` → `/app/media`

8. **Auto-restart**: Enable
9. **Dependency**: `gingerbread-db` (должен стартовать первым)
10. **Применить** и запустить

### Шаг 4: Проверка

1. **Container Manager → Container → gingerbread-bot → Details → Log**
2. Должны увидеть:
   ```
   ℹ️  Production mode (переменные окружения из Docker)
   🍪 Запуск бота для заказа пряников...
   🤖 Бот запущен в режиме polling
   ```

---

## Обновление бота

### Через SSH (docker-compose)
```bash
cd /volume1/docker/gingerbread-bot
git pull  # если используете git
sudo docker-compose down
sudo docker-compose up -d --build
```

### Через UI
1. Остановите контейнер `gingerbread-bot`
2. Пересоберите образ:
   ```bash
   cd /volume1/docker/gingerbread-bot
   sudo docker build -t gingerbread-bot:latest .
   ```
3. В Container Manager → Container → gingerbread-bot → Action → Reset
4. Запустите контейнер

---

## Troubleshooting

### Ошибка "TELEGRAM_BOT_TOKEN не установлена"
- **Через UI**: Проверьте, что переменная добавлена в Environment Variables контейнера
- **Через docker-compose**: Убедитесь что `.env` файл существует в папке проекта

### Контейнер постоянно перезапускается
```bash
sudo docker-compose logs bot
```
Проверьте логи на наличие ошибок подключения к БД или неверных переменных.

### База данных недоступна
```bash
sudo docker-compose exec postgres psql -U gingerbread_user -d gingerbread_bot -c "SELECT 1;"
```

### Узнать свой Telegram User ID
Напишите боту `@userinfobot` в Telegram, он покажет ваш ID.

---

## Безопасность

⚠️ **Важно**: Не коммитьте файл `.env` с реальным токеном в Git!

Файл `.env` должен находиться только на NAS и в `.gitignore`.

Для работы через Git создайте `.env.example` с шаблоном:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
ADMIN_USER_IDS=your_telegram_user_id
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/db
```
