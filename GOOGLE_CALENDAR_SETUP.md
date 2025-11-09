# Настройка Google Calendar для автоматического добавления заказов

## Что это дает?
При создании заказа автоматически создается событие в вашем Google Calendar с:
- Периодом изготовления (от начала работы до даты выдачи)
- Всей информацией о заказе (клиент, телефон, тип, количество, повод)
- Напоминаниями (за сутки и за час до выдачи)

## Пошаговая настройка

### 1. Создайте проект в Google Cloud Console

1. Перейдите на https://console.cloud.google.com/
2. Нажмите **Select a project** → **New Project**
3. Введите название проекта (например, "Gingerbread Bot")
4. Нажмите **Create**

### 2. Включите Google Calendar API

1. В боковом меню выберите **APIs & Services** → **Library**
2. Найдите "Google Calendar API"
3. Нажмите на него и затем **Enable**

### 3. Создайте OAuth 2.0 Credentials

1. В боковом меню выберите **APIs & Services** → **Credentials**
2. Нажмите **Create Credentials** → **OAuth client ID**
3. Если появится предупреждение о consent screen:
   - Нажмите **Configure Consent Screen**
   - Выберите **External** и нажмите **Create**
   - Заполните обязательные поля:
     - App name: "Gingerbread Bot"
     - User support email: ваш email
     - Developer contact: ваш email
   - Нажмите **Save and Continue**
   - На странице Scopes нажмите **Save and Continue**
   - На странице Test users добавьте свой email
   - Нажмите **Save and Continue**
4. Вернитесь в **Credentials** и снова нажмите **Create Credentials** → **OAuth client ID**
5. Выберите **Application type**: **Desktop app**
6. Введите название (например, "Gingerbread Bot Desktop")
7. Нажмите **Create**
8. Скачайте JSON файл с credentials (кнопка **Download JSON**)

### 4. Сохраните credentials в проект

Скопируйте скачанный JSON файл в папку `config/` вашего проекта с именем `credentials.json`:

```bash
cp ~/Downloads/client_secret_*.json config/credentials.json
```

### 5. Включите интеграцию в .env

Отредактируйте файл `.env`:

```bash
GOOGLE_CALENDAR_ENABLED=True
GOOGLE_CALENDAR_ID=primary  # или ID конкретного календаря
```

Если хотите использовать не основной календарь:
1. Откройте Google Calendar
2. Нажмите на календарь → Settings and sharing
3. Скопируйте Calendar ID из раздела "Integrate calendar"
4. Вставьте его в `GOOGLE_CALENDAR_ID=`

### 6. Перезапустите бота

```bash
./scripts/start.sh
```

### 7. Первая авторизация

При создании первого заказа с включенной интеграцией:
1. В терминале появится ссылка или автоматически откроется браузер
2. Войдите в свой Google аккаунт
3. Разрешите доступ к Google Calendar
4. Токен будет сохранен в `config/token.json` для последующих использований

**Важно:** Файл `token.json` содержит токен доступа. Добавьте его в `.gitignore`!

## Проверка работы

1. Создайте тестовый заказ через бота
2. Откройте Google Calendar
3. Вы должны увидеть новое событие с деталями заказа

## Устранение проблем

### Ошибка "credentials.json not found"
- Убедитесь, что файл находится в `config/credentials.json`
- Проверьте что путь к файлу правильный

### Ошибка авторизации
- Удалите `config/token.json`
- Перезапустите бота и пройдите авторизацию заново

### Событие не создается
- Проверьте что `GOOGLE_CALENDAR_ENABLED=True` в `.env`
- Посмотрите логи бота на наличие ошибок
- Убедитесь что Google Calendar API включен в Cloud Console

## Дополнительно

### Изменение цвета событий
В файле `bot/utils/google_calendar.py` строка:
```python
'colorId': '5',  # Желтый цвет (можно изменить 1-11)
```

Доступные цвета (ID):
- 1: Лавандовый
- 2: Шалфей
- 3: Виноградный
- 4: Фламинго
- 5: Банановый (желтый)
- 6: Мандариновый (оранжевый)
- 7: Павлиний (бирюзовый)
- 8: Графитовый (серый)
- 9: Черничный (синий)
- 10: Базиликовый (зеленый)
- 11: Томатный (красный)

### Изменение напоминаний
В файле `bot/utils/google_calendar.py` раздел `reminders`:
```python
'reminders': {
    'useDefault': False,
    'overrides': [
        {'method': 'popup', 'minutes': 24 * 60},  # За день
        {'method': 'popup', 'minutes': 60},       # За час
    ],
},
```

Можете добавить больше напоминаний или изменить время.
