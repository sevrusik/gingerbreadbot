from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    # Выбор типа пряников
    choosing_type = State()
    
    # Уточнение темы для тематических пряников
    choosing_theme = State()
    
    # Количество
    entering_quantity = State()
    
    # Дата готовности
    entering_date = State()
    
    # Повод/описание
    entering_occasion = State()
    
    # Контактный телефон
    entering_phone = State()
    
    # Подтверждение заказа
    confirming_order = State()


class AdminStates(StatesGroup):
    # Админские состояния
    viewing_orders = State()
    changing_order_status = State()
    sending_broadcast = State()