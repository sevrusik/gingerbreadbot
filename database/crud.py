from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy import select, update, and_
from datetime import datetime, timedelta
from typing import Optional, List

from database.models import Base, Customer, Order, Calendar, OrderStatus
from bot.utils.validators import generate_order_number
from config.settings import settings

# Создание движка базы данных
if settings.database_url.startswith("sqlite"):
    # Для SQLite используем aiosqlite
    DATABASE_URL = settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")
else:
    DATABASE_URL = settings.database_url

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    query_cache_size=500,  # Кэш скомпилированных SQL запросов (экономит CPU)
    pool_pre_ping=True,     # Проверка соединений перед использованием
    pool_recycle=3600       # Переиспользование соединений (1 час)
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Получение сессии базы данных"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# CRUD операции для клиентов

async def get_customer_by_telegram_id(telegram_user_id: int) -> Optional[Customer]:
    """Получение клиента по Telegram ID"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Customer).where(Customer.telegram_user_id == telegram_user_id)
        )
        return result.scalar_one_or_none()


async def get_or_create_customer(telegram_user_id: int, name: str = None) -> Customer:
    """Получение или создание клиента"""
    async with AsyncSessionLocal() as session:
        # Ищем существующего клиента
        result = await session.execute(
            select(Customer).where(Customer.telegram_user_id == telegram_user_id)
        )
        customer = result.scalar_one_or_none()
        
        if customer:
            # Обновляем имя если оно изменилось
            if name and customer.name != name:
                customer.name = name
                await session.commit()
                await session.refresh(customer)
            return customer
        
        # Создаем нового клиента
        customer = Customer(
            telegram_user_id=telegram_user_id,
            name=name
        )
        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return customer


async def update_customer_phone(telegram_user_id: int, phone: str):
    """Обновление телефона клиента"""
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Customer)
            .where(Customer.telegram_user_id == telegram_user_id)
            .values(phone=phone)
        )
        await session.commit()


async def update_customer_language(telegram_user_id: int, language: str):
    """Обновление языка клиента"""
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Customer)
            .where(Customer.telegram_user_id == telegram_user_id)
            .values(language=language)
        )
        await session.commit()


async def get_customer_language(telegram_user_id: int) -> str:
    """Получение языка клиента"""
    customer = await get_customer_by_telegram_id(telegram_user_id)
    if customer and customer.language:
        return customer.language
    return "ru"  # По умолчанию русский


# CRUD операции для заказов

async def create_order(
    customer_id: int,
    product_type: str,
    quantity: int,
    price_per_item: float,
    total_price: float,
    delivery_date: datetime,
    phone: str,
    theme_description: str = "",
    occasion: str = "",
    telegram_message_id: int = None
) -> Order:
    """Создание нового заказа"""
    async with AsyncSessionLocal() as session:
        order = Order(
            order_number=generate_order_number(),
            customer_id=customer_id,
            product_type=product_type,
            theme_description=theme_description,
            quantity=quantity,
            price_per_item=price_per_item,
            total_price=total_price,
            delivery_date=delivery_date,
            occasion=occasion,
            phone=phone,
            telegram_message_id=telegram_message_id,
            status=OrderStatus.NEW.value
        )
        
        session.add(order)
        await session.commit()
        await session.refresh(order)
        
        # Обновляем календарь
        await update_calendar_booking(delivery_date, quantity)
        
        return order


async def get_order_by_number(order_number: str) -> Optional[Order]:
    """Получение заказа по номеру"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order)
            .options(selectinload(Order.customer))
            .where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()


async def get_orders_by_customer(customer_id: int) -> List[Order]:
    """Получение всех заказов клиента"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order)
            .where(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()


async def get_orders_by_date(date: datetime) -> List[Order]:
    """Получение заказов на определенную дату"""
    async with AsyncSessionLocal() as session:
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        result = await session.execute(
            select(Order).where(
                and_(
                    Order.delivery_date >= start_date,
                    Order.delivery_date < end_date,
                    Order.status != OrderStatus.CANCELLED.value
                )
            ).order_by(Order.created_at)
        )
        return result.scalars().all()


async def get_active_orders() -> List[Order]:
    """Получение активных заказов"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order).where(
                Order.status.in_([
                    OrderStatus.NEW.value,
                    OrderStatus.CONFIRMED.value,
                    OrderStatus.IN_PROGRESS.value,
                    OrderStatus.READY.value
                ])
            ).order_by(Order.delivery_date, Order.created_at)
        )
        return result.scalars().all()


async def get_active_orders_by_customer(customer_id: int) -> List[Order]:
    """Получение активных заказов клиента"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order).where(
                and_(
                    Order.customer_id == customer_id,
                    Order.status.in_([
                        OrderStatus.NEW.value,
                        OrderStatus.CONFIRMED.value,
                        OrderStatus.IN_PROGRESS.value,
                        OrderStatus.READY.value
                    ])
                )
            ).order_by(Order.delivery_date, Order.created_at)
        )
        return result.scalars().all()


async def update_order_status(order_id: int, status: OrderStatus):
    """Обновление статуса заказа"""
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(
                status=status.value,
                completed_at=datetime.utcnow() if status == OrderStatus.COMPLETED else None
            )
        )
        await session.commit()


# CRUD операции для календаря

async def get_or_create_calendar_day(date: datetime) -> Calendar:
    """Получение или создание дня в календаре"""
    async with AsyncSessionLocal() as session:
        date_only = date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        result = await session.execute(
            select(Calendar).where(Calendar.date == date_only)
        )
        calendar_day = result.scalar_one_or_none()
        
        if not calendar_day:
            calendar_day = Calendar(
                date=date_only,
                available_slots=50,  # По умолчанию 50 заказов в день
                booked_orders=0,
                is_working_day=True
            )
            session.add(calendar_day)
            await session.commit()
            await session.refresh(calendar_day)
        
        return calendar_day


async def check_date_availability(date: datetime, required_quantity: int = 1) -> bool:
    """Проверка доступности даты"""
    calendar_day = await get_or_create_calendar_day(date)
    return calendar_day.is_available(required_quantity)


async def update_calendar_booking(date: datetime, quantity: int):
    """Обновление бронирования в календаре"""
    async with AsyncSessionLocal() as session:
        date_only = date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Получаем или создаем день
        calendar_day = await get_or_create_calendar_day(date)
        
        # Обновляем количество забронированных заказов
        await session.execute(
            update(Calendar)
            .where(Calendar.date == date_only)
            .values(booked_orders=Calendar.booked_orders + quantity)
        )
        await session.commit()


async def get_calendar_days(start_date: datetime, end_date: datetime) -> List[Calendar]:
    """Получение дней календаря в диапазоне"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Calendar).where(
                and_(
                    Calendar.date >= start_date,
                    Calendar.date <= end_date
                )
            ).order_by(Calendar.date)
        )
        return result.scalars().all()


# Вспомогательные функции

async def get_daily_stats(date: datetime) -> dict:
    """Получение статистики за день"""
    orders = await get_orders_by_date(date)
    
    stats = {
        "total_orders": len(orders),
        "total_items": sum(order.quantity for order in orders),
        "total_revenue": sum(order.total_price for order in orders),
        "orders_by_type": {},
        "orders_by_status": {}
    }
    
    for order in orders:
        # По типам
        if order.product_type not in stats["orders_by_type"]:
            stats["orders_by_type"][order.product_type] = 0
        stats["orders_by_type"][order.product_type] += order.quantity
        
        # По статусам
        if order.status not in stats["orders_by_status"]:
            stats["orders_by_status"][order.status] = 0
        stats["orders_by_status"][order.status] += 1
    
    return stats