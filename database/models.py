from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()


class OrderStatus(PyEnum):
    NEW = "new"                    # Новый заказ
    CONFIRMED = "confirmed"        # Подтвержден
    IN_PROGRESS = "in_progress"    # В работе
    READY = "ready"               # Готов
    COMPLETED = "completed"       # Выполнен
    CANCELLED = "cancelled"       # Отменен


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(Integer, unique=True, index=True)
    phone = Column(String(20))
    name = Column(String(100))
    language = Column(String(2), default="ru")  # ru, en, uk
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с заказами
    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(20), unique=True, index=True)
    
    # Связь с клиентом
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")
    
    # Основная информация
    product_type = Column(String(50))           # classic, coloring, numbers, themed
    theme_description = Column(Text)            # Описание темы/дизайна
    quantity = Column(Integer)
    price_per_item = Column(Float)
    total_price = Column(Float)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow)
    delivery_date = Column(DateTime)            # Когда должно быть готово
    completed_at = Column(DateTime, nullable=True)
    
    # Статус и заметки
    status = Column(String(20), default=OrderStatus.NEW.value)
    notes = Column(Text)                        # Особые пожелания
    occasion = Column(String(100))              # Повод (день рождения, садик и т.д.)
    
    # Контактная информация
    phone = Column(String(20))
    
    # Системная информация
    telegram_message_id = Column(Integer)
    is_rush_order = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"Order(#{self.order_number}, {self.product_type}, {self.quantity}шт)"


class Calendar(Base):
    __tablename__ = "calendar"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True)
    available_slots = Column(Integer, default=50)    # Максимум заказов в день
    booked_orders = Column(Integer, default=0)       # Забронировано
    is_working_day = Column(Boolean, default=True)   # Рабочий день
    notes = Column(Text)                             # Заметки (выходной, праздник и т.д.)
    
    def is_available(self, required_quantity: int = 1) -> bool:
        """Проверяет, доступна ли дата для заказа"""
        return (self.is_working_day and 
                self.booked_orders + required_quantity <= self.available_slots)