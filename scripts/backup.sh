#!/bin/bash

# Скрипт резервного копирования для gingerbread-bot

set -e

echo "💾 Создание резервной копии..."

# Переходим в директорию проекта
cd "$(dirname "$0")/.."

# Создаем директорию для бэкапов если её нет
mkdir -p backups

# Формат даты для имени файла
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/backup_${DATE}"
BACKUP_ARCHIVE="backups/gingerbread_backup_${DATE}.tar.gz"

# Создаем временную директорию для бэкапа
mkdir -p "$BACKUP_DIR"

echo "📁 Подготовка файлов для бэкапа..."

# Копируем базу данных
if [ -f "database/orders.db" ]; then
    echo "🗄️ Копирование базы данных..."
    cp database/orders.db "$BACKUP_DIR/"
else
    echo "⚠️ База данных не найдена"
fi

# Копируем конфигурацию (без секретных данных)
echo "⚙️ Копирование конфигурации..."
if [ -f ".env" ]; then
    # Создаем копию .env без секретных токенов
    grep -v "TOKEN\|PASSWORD\|SECRET" .env > "$BACKUP_DIR/.env.template" || true
fi

# Копируем логи (последние 7 дней)
if [ -d "logs" ]; then
    echo "📝 Копирование логов..."
    mkdir -p "$BACKUP_DIR/logs"
    find logs -name "*.log" -mtime -7 -exec cp {} "$BACKUP_DIR/logs/" \;
fi

# Создаем информационный файл
echo "📋 Создание информации о бэкапе..."
cat > "$BACKUP_DIR/backup_info.txt" << EOF
Gingerbread Bot Backup
======================
Дата создания: $(date)
Версия: $(git describe --tags --always 2>/dev/null || echo "unknown")
Хост: $(hostname)
Пользователь: $(whoami)

Содержимое:
- База данных SQLite
- Конфигурация (без секретов)
- Логи (последние 7 дней)

Для восстановления:
1. Распакуйте архив
2. Скопируйте orders.db в database/
3. Восстановите .env из шаблона
4. Перезапустите бота
EOF

# Подсчитываем статистику базы данных
if [ -f "database/orders.db" ]; then
    echo "" >> "$BACKUP_DIR/backup_info.txt"
    echo "Статистика базы данных:" >> "$BACKUP_DIR/backup_info.txt"
    echo "======================" >> "$BACKUP_DIR/backup_info.txt"
    
    # Активируем виртуальное окружение если есть
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Получаем статистику через SQLite
    sqlite3 database/orders.db << SQL >> "$BACKUP_DIR/backup_info.txt" 2>/dev/null || echo "Ошибка получения статистики" >> "$BACKUP_DIR/backup_info.txt"
.mode line
SELECT 
    'Всего клиентов: ' || COUNT(*) as customers
FROM customers;

SELECT 
    'Всего заказов: ' || COUNT(*) as total_orders
FROM orders;

SELECT 
    'Активных заказов: ' || COUNT(*) as active_orders
FROM orders 
WHERE status IN ('new', 'confirmed', 'in_progress', 'ready');

SELECT 
    'Общая выручка: ' || ROUND(SUM(total_price), 2) || '€' as total_revenue
FROM orders 
WHERE status != 'cancelled';

SELECT 
    'Размер БД: ' || ROUND(page_count * page_size / 1024.0 / 1024.0, 2) || ' MB' as db_size
FROM pragma_page_count(), pragma_page_size();
SQL
fi

# Создаем архив
echo "📦 Создание архива..."
tar -czf "$BACKUP_ARCHIVE" -C backups "backup_${DATE}"

# Удаляем временную директорию
rm -rf "$BACKUP_DIR"

# Получаем размер архива
ARCHIVE_SIZE=$(du -h "$BACKUP_ARCHIVE" | cut -f1)

echo "✅ Резервная копия создана!"
echo "📁 Файл: $BACKUP_ARCHIVE"
echo "💾 Размер: $ARCHIVE_SIZE"

# Очистка старых бэкапов (оставляем последние 30)
echo "🧹 Очистка старых бэкапов..."
find backups -name "gingerbread_backup_*.tar.gz" -mtime +30 -delete 2>/dev/null || true

BACKUP_COUNT=$(find backups -name "gingerbread_backup_*.tar.gz" | wc -l)
echo "📚 Всего бэкапов: $BACKUP_COUNT"

echo ""
echo "🎯 Рекомендации:"
echo "- Регулярно копируйте бэкапы в облачное хранилище"
echo "- Тестируйте восстановление из бэкапов"
echo "- Настройте автоматическое создание бэкапов в crontab"
echo ""
echo "Пример для crontab (ежедневно в 2:00):"
echo "0 2 * * * /path/to/gingrebread-bot/scripts/backup.sh"