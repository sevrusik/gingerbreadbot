# ⚠️ SECURITY INCIDENT - Token Exposure

## Что произошло

**Дата**: 2025-11-18
**Проблема**: Telegram Bot Token был случайно закоммичен в публичный Git репозиторий

**Скомпрометированный токен**: `8313090422:AAFQIjNFVRHRIgnY4JRTN3CUXgA5r8mSvlI`

**Затронутые коммиты**:
- `68318c4` - Add Synology NAS deployment documentation and script
- Файл: `SYNOLOGY_DEPLOYMENT.md` (строка 112)

---

## ✅ Немедленные действия (ОБЯЗАТЕЛЬНО)

### 1. Перегенерируйте токен бота

**Важно**: Старый токен скомпрометирован и должен быть немедленно отозван!

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/mybots`
3. Выберите вашего бота (Gingerbread Bot)
4. Нажмите **API Token**
5. Нажмите **Revoke current token** (отозвать текущий токен)
6. Скопируйте новый токен

### 2. Обновите токен в .env файле

На вашем Synology NAS:

```bash
# Подключитесь по SSH
ssh your_username@synology_ip

# Откройте .env файл
cd /volume1/docker/gingerbread-bot
nano .env

# Замените TELEGRAM_BOT_TOKEN на новый
# Сохраните: Ctrl+O, Enter, Ctrl+X
```

### 3. Перезапустите бота с новым токеном

```bash
cd /volume1/docker/gingerbread-bot
sudo docker-compose down
sudo docker-compose up -d
sudo docker-compose logs -f bot
```

Вы должны увидеть:
```
🍪 Запуск бота для заказа пряников...
🤖 Бот запущен в режиме polling
```

---

## 🔧 Что было исправлено в коде

### Исправленные файлы (коммит `TODO`)

1. **SYNOLOGY_DEPLOYMENT.md**
   - Заменен реальный токен на `your_bot_token_here`

2. **.env.example**
   - Обновлен шаблон с примером переменных
   - Добавлены комментарии для Docker/PostgreSQL

---

## 🛡️ Меры предотвращения

### Что уже настроено

✅ `.env` файл в `.gitignore`
✅ `.env` файл в `.dockerignore`
✅ `.env.example` с шаблоном (без секретов)

### Рекомендации на будущее

1. **Никогда не коммитьте файлы с секретами**
   - `.env`
   - `credentials.json`
   - `token.json`
   - Любые файлы с паролями/токенами

2. **Проверяйте перед коммитом**
   ```bash
   git diff  # Проверьте изменения перед коммитом
   ```

3. **Используйте pre-commit hooks**
   ```bash
   # Установите detect-secrets
   pip install detect-secrets
   detect-secrets scan
   ```

4. **Для примеров используйте плейсхолдеры**
   - `your_token_here`
   - `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - `example_value`

---

## 📝 История очистки репозитория

### Опция 1: Удалить из последних коммитов (если не критично)

Токен уже удален из файлов в новом коммите. Старые коммиты содержат токен в истории, но он отозван и больше не работает.

### Опция 2: Полная очистка истории (опционально)

⚠️ **Внимание**: Это перепишет историю Git. Используйте только если необходимо.

```bash
# Установите git-filter-repo
brew install git-filter-repo  # macOS
# или
pip install git-filter-repo

# Замените токен во всей истории
git filter-repo --replace-text <(echo "8313090422:AAFQIjNFVRHRIgnY4JRTN3CUXgA5r8mSvlI==>your_bot_token_here")

# Force push (только если репозиторий приватный и вы единственный разработчик)
git push --force --all
```

---

## ✅ Checklist восстановления

- [ ] Токен бота отозван через @BotFather
- [ ] Новый токен получен
- [ ] `.env` файл обновлен на NAS
- [ ] Бот перезапущен с новым токеном
- [ ] Бот успешно запустился и отвечает
- [ ] Проверено что токена нет в новых файлах
- [ ] Документация обновлена (этот файл прочитан)

---

## 📞 Контакты

Если у вас возникли вопросы или проблемы с восстановлением доступа, обратитесь к документации Telegram Bot API:
- https://core.telegram.org/bots/api
- https://core.telegram.org/bots/faq#how-do-i-get-my-bot-token

---

## 📚 Дополнительные материалы

- [Telegram Bot Security Best Practices](https://core.telegram.org/bots/faq#security)
- [GitHub Secrets Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
