# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Telegram bot for automating gingerbread cookie orders. Written in Python using aiogram 3.4, it manages the complete order workflow from customer requests to admin fulfillment tracking. The bot presents itself as "мастер Любовь" (Master Lyubov) for a personalized customer experience.

## Development Commands

### Initial Setup
```bash
# First-time setup (creates venv, installs dependencies, generates .env template)
./scripts/setup.sh

# After setup, edit .env with your bot token and admin IDs
# Note: ADMIN_USER_IDS in .env (plural) becomes admin_user_ids in settings
```

### Project Structure
```
gingerbread-bot/
├── bot/
│   ├── handlers/      # start.py, order.py, admin.py (routers)
│   ├── keyboards/     # UI keyboards and button layouts
│   ├── middlewares/   # LanguageMiddleware for caching
│   ├── states/        # FSM state definitions
│   └── utils/         # texts.py, validators.py, order_cache.py, photo_cache.py
├── config/            # settings.py, database.py, credentials.json (gitignored)
├── database/          # models.py, crud.py, orders.db
├── media/
│   └── examples/      # Product type images (classic.jpg, coloring.jpg, etc.)
├── scripts/           # setup.sh, start.sh, backup.sh
└── logs/              # Auto-generated timestamped log files
```

### Running the Bot
```bash
# Recommended method (handles venv activation, logging, validation)
./scripts/start.sh

# Direct execution
python run.py
```

### Database Operations
```bash
# Check database integrity
sqlite3 database/orders.db "PRAGMA integrity_check;"

# View orders
sqlite3 database/orders.db "SELECT * FROM orders;"

# Daily stats
sqlite3 database/orders.db "SELECT COUNT(*), SUM(total_price) FROM orders WHERE DATE(created_at) = DATE('now');"
```

### Backup
```bash
# Create manual backup
./scripts/backup.sh
```

## Architecture

### Middleware System

**LanguageMiddleware** (`bot/middlewares/language.py`) - Registered in `bot/main.py:115-117`:
- Loads user language **once** per update from database
- Caches in handler context: `data['user_lang']`
- Access via `get_user_lang(kwargs)` helper from `bot/utils/context.py`
- Reduces DB queries by 60-70% compared to querying language in each handler

**Pattern**: All handlers accept `**kwargs` and use `lang = get_user_lang(kwargs)` instead of calling `get_customer_language()`.

### Caching Layer

**Order Cache** (`bot/utils/order_cache.py`):
- TTL cache (60 seconds) for active customer orders
- Used in: `start.py`, `order.py`, `admin.py`
- Methods: `get()`, `set()`, `invalidate()`, `cleanup()`
- **Critical**: Invalidate cache after order creation/status changes via `order_cache.invalidate(customer_id)`

**Photo Cache** (`bot/utils/photo_cache.py`):
- Caches Telegram file_id for product type images
- Avoids re-uploading same images from disk
- Auto-populated on first image send in `order.py:105-127`

**Query Cache** (`database/crud.py:18-24`):
- SQLAlchemy compiled query cache: `query_cache_size=500`
- Connection pool with `pool_pre_ping=True` and `pool_recycle=3600`
- Reduces CPU overhead for repeated queries by 5-10%

### Handler Flow and Router Registration Order

**Critical**: Handlers are registered in `bot/main.py:register_handlers()` in this specific order:
1. Middleware registration (Language caching)
2. `start.router` - Entry point and navigation
3. `order.router` - Order creation flow
4. `admin.router` - Administrative functions

The order matters because aiogram processes routers sequentially. Start handlers must come first to catch `/start` and navigation callbacks before order flow.

### FSM State Machine

The bot uses aiogram's FSM (Finite State Machine) for multi-step conversations. Order flow states defined in `bot/states/order_states.py`:

```
OrderStates:
  choosing_type → choosing_theme → entering_quantity →
  entering_date → entering_occasion → entering_phone → confirming_order
```

When working with states:
- Always call `await state.clear()` when returning to main menu
- Store intermediate data with `await state.update_data(key=value)`
- Retrieve with `data = await state.get_data()`

**Order flow navigation** (`bot/handlers/order.py`):
- Callback data patterns: `type_{key}`, `theme_{name}`, `custom_theme`
- Urgent orders skip minimum preparation time validation
- Themed/urgent orders require theme description before proceeding to quantity
- Classic/coloring/numbers orders skip theme selection

### Database Layer Architecture

**Session Management**: Uses SQLAlchemy async ORM with `AsyncSessionLocal` session factory. Each CRUD function in `database/crud.py` creates its own session using:
```python
async with AsyncSessionLocal() as session:
    # operations
```

**Important**: Do not pass sessions between functions. Each CRUD operation is self-contained.

**Models** (`database/models.py`):
- `Customer` - One-to-many with `Order` via `customer_id`
- `Order` - Core business entity with status tracking
  - Status enum: `NEW` → `CONFIRMED` → `IN_PROGRESS` → `READY` → `COMPLETED` (or `CANCELLED`)
  - `is_rush_order` flag for urgent orders
- `Calendar` - Date availability tracking with slot management
  - Default 50 slots per day (`available_slots`)
  - `is_available(required_quantity)` method checks remaining capacity

**Calendar Booking Logic**: When creating orders, `create_order()` automatically calls `update_calendar_booking()` to increment `booked_orders` for the delivery date. This maintains slot availability tracking.

### Configuration System

Settings loaded via Pydantic from `.env` in `config/settings.py`. The global `settings` instance is imported throughout the codebase.

**Gingerbread types** defined in `GINGERBREAD_TYPES` dict with pricing:
- `classic` - Base price (2.0 EUR default)
- `coloring` - Higher price (3.5 EUR), includes art supplies
- `numbers` - Base price, birthday-specific
- `themed` - Base price, requires theme description
- `urgent` - Double base price, bypasses minimum preparation time

**Popular themes** in `config/settings.py:POPULAR_THEMES` - preset theme options shown to users when ordering themed gingerbreads

### Text Management and Localization

**Multi-language support** via `bot/utils/translations.py`:
- `get_text(key, lang, **kwargs)` - Primary function for all user-facing text
- Supports: Russian (`ru`), English (`en`), Ukrainian (`uk`)
- Translations stored in `TRANSLATIONS` dict with fallback to Russian
- All handlers use language from middleware context: `lang = get_user_lang(kwargs)`

**Legacy texts** in `bot/utils/texts.py` (`BotTexts` class):
- Contains some Russian-only texts (being migrated to translations system)
- Prefer using `get_text()` for new features to ensure multi-language support

**Welcome message builder** (`bot/utils/welcome_builder.py`):
- `build_welcome_message(customer, active_orders, lang, user_id)`
- Unified function for constructing welcome screens with/without active orders
- Returns tuple: `(text, keyboard)`
- Used by: `start.py` handlers to avoid code duplication

### Keyboard Patterns

Keyboards defined in `bot/keyboards/` modules:
- `main_menu.py` - Main navigation and order flow keyboards
- `order_flow.py` - Order-specific inline keyboards

**Common keyboard functions**:
- `gingerbread_types()` - Inline keyboard for product type selection
- `popular_themes()` - Inline keyboard with preset themes + custom option
- `confirmation_keyboard()` - Yes/No confirmation buttons
- `phone_keyboard()` - Reply keyboard with phone number request button

**Pattern**: Use `InlineKeyboardMarkup` for callback-based navigation, `ReplyKeyboardMarkup` for data collection (like phone numbers)

### Admin Permission Pattern

**Multi-admin support**: Configure via comma-separated `ADMIN_USER_IDS` in `.env` (e.g., `123456,789012`). Access via `settings.admin_ids_list` property or `settings.is_admin(user_id)` method.

All admin handlers check permissions using:
```python
if not settings.is_admin(message.from_user.id):
    await message.answer("⛔️ Недостаточно прав")
    return
```

Admin commands: `/admin`, `/today`, `/tomorrow`, `/status <order_number> <new_status>`

**Bot commands setup** in `bot/main.py:setup_bot_commands()` - Different command menus for regular users vs admins, with admin-specific commands only visible to configured admin users

### Order Number Generation

Order numbers use format `YYMMDD-HHMM` (e.g., `240725-1430`) generated by `validators.generate_order_number()`. This ensures uniqueness and sortability.

### Phone Validation

Uses `phonenumbers` library in `bot/utils/validators.py`. Automatically handles Russian phone number formats (adds +7 prefix when needed). Always use `validate_phone()` before storing and `format_phone()` for display.

### Date Validation

`parse_date()` supports multiple formats: `dd.mm.yyyy`, `dd/mm/yyyy`, `dd-mm-yyyy`, and short forms without year. If year is omitted and date has passed this year, automatically uses next year.

`validate_date()` enforces minimum preparation time (`MIN_PREPARATION_DAYS` from settings, default 3) and maximum 1 year advance booking.

## Development Patterns

### Adding New Handler

1. Create handler file in `bot/handlers/` with a router:
```python
from aiogram import Router
from bot.utils.context import get_user_lang
router = Router()

@router.message(...)
async def handler_name(message: Message, **kwargs):
    lang = get_user_lang(kwargs)  # Get language from middleware cache
    # handler logic
```

2. Import and register in `bot/main.py:register_handlers()` (order matters!)

3. If multi-step, add states to `bot/states/order_states.py`

**Important**:
- Always include `**kwargs` parameter to receive middleware data
- Use `get_user_lang(kwargs)` instead of calling `get_customer_language()`
- Invalidate caches when creating/modifying orders: `order_cache.invalidate(customer_id)`

### Adding New CRUD Operation

Follow the pattern in `database/crud.py`:
```python
async def operation_name(...) -> ReturnType:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(...))
        # operations
        await session.commit()
        return result
```

Always create a new session within the function scope.

**Statistics and reporting** (`database/crud.py`):
- `get_daily_stats(date)` - Returns aggregated stats: total orders, items, revenue, breakdown by type and status
- `get_orders_by_date(date)` - Filters orders for specific delivery date (excludes cancelled)
- `get_active_orders()` - Returns all non-completed, non-cancelled orders sorted by delivery date
- `get_active_orders_by_customer(customer_id)` - Customer-specific active orders

### Database Migrations

This project uses SQLAlchemy models but appears to handle migrations through `init_db()` which creates tables if they don't exist. For production, consider adding Alembic migrations (already in requirements.txt).

To create migration:
```bash
# Initialize alembic (if not done)
alembic init database/migrations

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Logging

Logging configured in `bot/main.py` using Python's logging module. Log level controlled by `LOG_LEVEL` env var. When running via `./scripts/start.sh`, logs are saved to `logs/bot_YYYYMMDD_HHMMSS.log`.

**Bot lifecycle notifications**: On startup and shutdown, the bot automatically sends status messages to all configured admins via `on_startup()` and `on_shutdown()` handlers.

## MacMini M4 Deployment Notes

For production deployment on MacMini M4:
- Use launchd for auto-start (example plist in README)
- PostgreSQL recommended over SQLite for concurrent access
- Set up DDNS (DuckDNS) for stable external access
- Configure webhook mode instead of polling for better reliability

To switch to PostgreSQL:
```bash
brew install postgresql
brew services start postgresql
createdb gingerbread_bot

# Update .env:
DATABASE_URL=postgresql+asyncpg://user:password@localhost/gingerbread_bot
```

## Google Calendar Integration

**Optional feature** for auto-creating calendar events when orders are placed. Configured via `GOOGLE_CALENDAR_ENABLED` and `GOOGLE_CALENDAR_ID` in `.env`.

**Setup process** (detailed in `GOOGLE_CALENDAR_SETUP.md`):
1. Create Google Cloud project and enable Calendar API
2. Create OAuth 2.0 credentials, download `credentials.json` to `config/`
3. First run triggers browser auth flow, saves `token.json` for future use
4. **Important**: Add `config/token.json` and `config/credentials.json` to `.gitignore`

**Implementation** in `bot/utils/google_calendar.py`:
- `GoogleCalendarIntegration` class handles auth and event CRUD
- `create_order_event()` creates multi-day event from preparation start to delivery date
- Events include full order details, customer info, reminders
- Automatically called from order creation if enabled

**Integration point**: When creating orders via `database/crud.py:create_order()`, check if calendar integration is enabled and call `calendar_integration.create_order_event()` after successful order creation.

## Performance Optimizations

The bot implements several caching strategies to minimize database load:

1. **Language Middleware** - 1 DB query per update instead of 3-5 queries per message
2. **Order Cache** - 60-second TTL cache for active orders (reduces load by 70-80%)
3. **Photo Cache** - Telegram file_id reuse to avoid re-uploading images
4. **SQLAlchemy Query Cache** - Compiled query caching for 5-10% CPU savings

**Results**: Overall database load reduced by ~50-60% for frequent users.

**Adding more caching**:
- Follow patterns in `bot/utils/order_cache.py` and `bot/utils/photo_cache.py`
- Always implement cache invalidation for mutable data
- Use TTL for time-sensitive data (active orders, availability)
- Use permanent cache for immutable data (photos, translations)

## Testing

No test suite currently exists. When adding tests:
- Use pytest with pytest-asyncio for async handlers
- Mock aiogram's Message, CallbackQuery types
- Use in-memory SQLite for database tests: `sqlite+aiosqlite:///:memory:`
- Mock middleware context with `kwargs={'user_lang': 'ru'}` when testing handlers
