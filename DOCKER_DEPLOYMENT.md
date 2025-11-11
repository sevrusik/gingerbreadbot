# Docker развертывание на Synology NAS 218+

## Быстрый старт

### 1. Подготовка на NAS

Создайте папку через File Station:
```
/docker/gingerbread-bot/
```

### 2. Загрузите файлы проекта

Скопируйте все файлы проекта в `/docker/gingerbread-bot/` через:
- File Station (веб-интерфейс)
- SMB/CIFS (сетевая папка)
- SSH/SFTP

### 3. Настройте переменные окружения

Скопируйте `.env.docker` в `.env` и отредактируйте:

```bash
cp .env.docker .env
nano .env  # или через File Station
```

Обязательно измените:
```env
TELEGRAM_BOT_TOKEN=ваш_реальный_токен
ADMIN_USER_IDS=ваш_telegram_id
POSTGRES_PASSWORD=надежный_пароль
DATABASE_URL=postgresql://gingerbread_user:надежный_пароль@postgres:5432/gingerbread_bot
```

### 4. Запуск через SSH (Рекомендуется)

```bash
# Подключитесь к NAS
ssh admin@ip_вашего_nas

# Перейдите в папку проекта
cd /volume1/docker/gingerbread-bot

# Запустите контейнеры
sudo docker-compose up -d

# Проверьте статус
sudo docker-compose ps

# Посмотрите логи
sudo docker-compose logs -f bot
```

### 5. Запуск через Container Manager (GUI)

1. Откройте **Container Manager**
2. Перейдите в **Project**
3. Нажмите **Create** → **Create Project**
4. Project name: `gingerbread-bot`
5. Path: `/docker/gingerbread-bot`
6. Source: выберите `docker-compose.yml`
7. Нажмите **Done**

---

## Управление

### Остановить
```bash
sudo docker-compose stop
```

### Запустить
```bash
sudo docker-compose start
```

### Перезапустить
```bash
sudo docker-compose restart
```

### Пересобрать после изменений
```bash
sudo docker-compose up -d --build
```

### Посмотреть логи
```bash
# Все логи
sudo docker-compose logs

# Логи бота
sudo docker-compose logs bot

# Логи БД
sudo docker-compose logs postgres

# Следить за логами в реальном времени
sudo docker-compose logs -f bot
```

### Полная остановка и удаление
```bash
sudo docker-compose down
```

---

## Backup базы данных

### Создать backup
```bash
sudo docker exec gingerbread-db pg_dump -U gingerbread_user gingerbread_bot > backup_$(date +%Y%m%d).sql
```

### Восстановить из backup
```bash
cat backup_20241110.sql | sudo docker exec -i gingerbread-db psql -U gingerbread_user gingerbread_bot
```

### Автоматический backup (через Task Scheduler)

1. Control Panel → **Task Scheduler**
2. Create → **Scheduled Task** → **User-defined script**
3. Task: `Backup Gingerbread DB`
4. Schedule: Daily, 3:00 AM
5. Task Settings → User-defined script:
```bash
docker exec gingerbread-db pg_dump -U gingerbread_user gingerbread_bot > /volume1/docker/gingerbread-bot/backups/backup_$(date +\%Y\%m\%d).sql
```

---

## Мониторинг

### Статус контейнеров
```bash
sudo docker-compose ps
```

### Использование ресурсов
```bash
sudo docker stats
```

### Проверка здоровья БД
```bash
sudo docker exec gingerbread-db pg_isready -U gingerbread_user
```

### Подключение к БД
```bash
sudo docker exec -it gingerbread-db psql -U gingerbread_user -d gingerbread_bot
```

SQL команды:
```sql
-- Посмотреть таблицы
\dt

-- Посмотреть заказы
SELECT * FROM orders LIMIT 10;

-- Статистика
SELECT COUNT(*) as total_orders FROM orders;

-- Выход
\q
```

---

## Обновление бота

### Способ 1: Через Git (если используете)

```bash
cd /volume1/docker/gingerbread-bot
git pull
sudo docker-compose up -d --build
```

### Способ 2: Вручную

1. Загрузите новые файлы через File Station
2. Перезапустите контейнеры:
```bash
sudo docker-compose up -d --build
```

---

## Troubleshooting

### Бот не запускается

```bash
# Проверьте логи
sudo docker-compose logs bot

# Проверьте переменные окружения
sudo docker-compose config

# Пересоздайте контейнеры
sudo docker-compose down
sudo docker-compose up -d
```

### База данных не подключается

```bash
# Проверьте статус БД
sudo docker-compose ps postgres

# Проверьте здоровье
sudo docker exec gingerbread-db pg_isready -U gingerbread_user

# Проверьте логи БД
sudo docker-compose logs postgres
```

### Ошибка "Name or service not known"

Убедитесь что в `.env` используется `@postgres:5432`, а не внешний хост.

### Конфликт портов

Если порт 5432 уже занят:
```yaml
# В docker-compose.yml измените
ports:
  - "5433:5432"  # Используйте другой внешний порт
```

### Недостаточно места

```bash
# Проверьте место
df -h

# Очистите старые Docker образы
sudo docker system prune -a
```

---

## Структура папок

```
/volume1/docker/gingerbread-bot/
├── bot/                    # Код бота
├── config/                 # Конфигурация
├── database/               # Модели БД
├── media/                  # Изображения
├── data/
│   └── postgres/          # Данные PostgreSQL (создается автоматически)
├── logs/                   # Логи бота (создается автоматически)
├── backups/                # Backup базы данных (создайте вручную)
├── .env                    # Переменные окружения (создайте из .env.docker)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

---

## Безопасность

1. **Измените пароль PostgreSQL** в `.env` и `docker-compose.yml`
2. **Не публикуйте порт 5432** если не нужен внешний доступ
3. **Регулярный backup** базы данных
4. **Обновляйте образы**:
```bash
sudo docker-compose pull
sudo docker-compose up -d
```

---

## Мониторинг через Synology

1. **Docker** → Container Manager → Контейнеры
2. Выберите `gingerbread-bot` → **Details**
3. Вкладки:
   - **Terminal**: Консоль контейнера
   - **Log**: Логи в реальном времени
   - **Resource**: Использование CPU/RAM

---

## Производительность

### Synology DS218+ хватит для:
- ✅ 100-500 пользователей
- ✅ 1000-2000 заказов/месяц
- ✅ База данных до 10 GB

### Если нужна большая производительность:
- Увеличьте RAM на NAS (до 6 GB)
- Используйте SSD кэш для Docker
- Оптимизируйте запросы к БД

---

Готово! Бот работает на вашем Synology NAS 24/7.
