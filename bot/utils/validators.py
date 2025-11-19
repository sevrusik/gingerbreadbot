import re
from datetime import datetime
from typing import Optional
import phonenumbers


def validate_phone(phone: str) -> bool:
    """
    Валидация номера телефона
    Поддерживает: Кипр (+357), Россия (+7), Украина (+380)
    """
    try:
        # Убираем пробелы, дефисы, скобки
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)

        # Если номер уже начинается с +, используем как есть
        if clean_phone.startswith('+'):
            parsed = phonenumbers.parse(clean_phone, None)
            return phonenumbers.is_valid_number(parsed)

        # Определяем страну по началу номера
        # Кипр: 9XXXXXXX (8 цифр, начинается с 9) или 357XXXXXXXX (11 цифр)
        if clean_phone.startswith('9') and len(clean_phone) == 8:
            clean_phone = '+357' + clean_phone
        elif clean_phone.startswith('357') and len(clean_phone) == 11:
            clean_phone = '+' + clean_phone

        # Россия: 8XXXXXXXXXX или 7XXXXXXXXXX (11 цифр)
        elif clean_phone.startswith('8') and len(clean_phone) == 11:
            clean_phone = '+7' + clean_phone[1:]
        elif clean_phone.startswith('7') and len(clean_phone) == 11:
            clean_phone = '+' + clean_phone

        # Украина: 380XXXXXXXXX (12 цифр) или 0XXXXXXXXX (10 цифр)
        elif clean_phone.startswith('380') and len(clean_phone) == 12:
            clean_phone = '+' + clean_phone
        elif clean_phone.startswith('0') and len(clean_phone) == 10:
            clean_phone = '+38' + clean_phone

        # Если ничего не подошло, пробуем добавить код Кипра по умолчанию
        else:
            clean_phone = '+357' + clean_phone

        # Валидация через phonenumbers
        parsed = phonenumbers.parse(clean_phone, None)
        return phonenumbers.is_valid_number(parsed)
    except:
        return False


def parse_date(date_text: str) -> datetime:
    """Парсинг даты из текста"""
    # Убираем лишние пробелы
    date_text = date_text.strip()
    
    # Форматы для парсинга
    formats = [
        "%d.%m.%Y",    # 25.07.2024
        "%d.%m",       # 25.07
        "%d/%m/%Y",    # 25/07/2024
        "%d/%m",       # 25/07
        "%d-%m-%Y",    # 25-07-2024
        "%d-%m",       # 25-07
    ]
    
    current_year = datetime.now().year
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_text, fmt)
            
            # Если год не указан, используем текущий или следующий
            if fmt.count('%') == 2:  # Только день и месяц
                # Если дата уже прошла в этом году, используем следующий год
                this_year_date = parsed_date.replace(year=current_year)
                if this_year_date < datetime.now():
                    parsed_date = parsed_date.replace(year=current_year + 1)
                else:
                    parsed_date = this_year_date
            
            return parsed_date
            
        except ValueError:
            continue
    
    raise ValueError("Неверный формат даты")


def validate_date(date: datetime, is_urgent: bool = False) -> tuple[bool, Optional[str]]:
    """Валидация даты заказа"""
    from config.settings import settings
    from datetime import timedelta

    now = datetime.now()
    # Для срочных заказов используем min_preparation_days_urgent, для обычных - min_preparation_days
    min_days = settings.min_preparation_days_urgent if is_urgent else settings.min_preparation_days
    min_date = now + timedelta(days=min_days)
    max_date = now + timedelta(days=365)  # Не более года вперед

    if date < min_date:
        return False, f"Минимальный срок изготовления: {min_days} дней"

    if date > max_date:
        return False, "Слишком далекая дата. Принимаем заказы на год вперед"

    return True, None


def format_phone(phone: str) -> str:
    """Форматирование номера телефона для отображения"""
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    except:
        return phone


def generate_order_number() -> str:
    """Генерация номера заказа"""
    from datetime import datetime
    now = datetime.now()
    # Формат: YYMMDD-HHMM (например: 240725-1430)
    return now.strftime("%y%m%d-%H%M")


def calculate_price(product_type: str, quantity: int, is_rush: bool = False, price_per_item: float = None) -> float:
    """Расчет стоимости заказа

    Args:
        product_type: тип пряника
        quantity: количество
        is_rush: срочный заказ
        price_per_item: цена за единицу (для типов с подтипами передается явно)
    """
    from config.settings import GINGERBREAD_TYPES, settings

    # Если цена передана явно (для типов с подтипами) - используем её
    if price_per_item is not None:
        base_price = price_per_item
    else:
        # Иначе берем из конфигурации
        type_data = GINGERBREAD_TYPES[product_type]
        if "price" in type_data:
            base_price = type_data["price"]
        else:
            # Для типов с подтипами нужно передавать price_per_item
            raise ValueError(f"Для типа {product_type} нужно передать price_per_item")

    total = base_price * quantity

    if is_rush:
        total *= settings.rush_order_multiplier

    return round(total, 2)