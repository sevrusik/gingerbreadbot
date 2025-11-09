"""
Интеграция с Google Calendar для автоматического добавления заказов
"""
import os
from datetime import datetime, timedelta
from typing import Optional
import logging

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import settings

logger = logging.getLogger(__name__)

# Область доступа для чтения и записи в календарь
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarIntegration:
    """Класс для работы с Google Calendar API"""

    def __init__(self):
        self.creds = None
        self.service = None
        self.calendar_id = settings.google_calendar_id if hasattr(settings, 'google_calendar_id') else 'primary'

    def authenticate(self):
        """Аутентификация в Google Calendar API"""
        token_file = 'config/token.json'
        creds_file = 'config/credentials.json'

        # Проверяем существующий токен
        if os.path.exists(token_file):
            self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)

        # Если токена нет или он недействителен
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Не удалось обновить токен: {e}")
                    return False
            else:
                if not os.path.exists(creds_file):
                    logger.error(f"Файл credentials.json не найден в {creds_file}")
                    return False

                try:
                    flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                except Exception as e:
                    logger.error(f"Ошибка аутентификации: {e}")
                    return False

            # Сохраняем токен для последующего использования
            with open(token_file, 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
            return True
        except Exception as e:
            logger.error(f"Не удалось создать сервис Calendar API: {e}")
            return False

    def create_order_event(
        self,
        order_number: str,
        customer_name: str,
        product_type: str,
        quantity: int,
        delivery_date: datetime,
        phone: str,
        occasion: str = "",
        preparation_days: int = 3
    ) -> Optional[str]:
        """
        Создает событие в Google Calendar для заказа

        Args:
            order_number: Номер заказа
            customer_name: Имя клиента
            product_type: Тип пряников
            quantity: Количество
            delivery_date: Дата готовности/выдачи
            phone: Телефон клиента
            occasion: Повод
            preparation_days: Дней на изготовление (для расчета начала работы)

        Returns:
            ID созданного события или None при ошибке
        """
        if not self.service:
            if not self.authenticate():
                logger.error("Не удалось аутентифицироваться в Google Calendar")
                return None

        # Дата начала изготовления (за N дней до выдачи)
        start_date = delivery_date - timedelta(days=preparation_days)

        # Формируем описание события
        description = f"""📋 Заказ #{order_number}

👤 Клиент: {customer_name}
📱 Телефон: {phone}
🍪 Тип: {product_type}
📦 Количество: {quantity} шт
🎉 Повод: {occasion if occasion else 'Не указан'}

📅 Дата выдачи: {delivery_date.strftime('%d.%m.%Y')}
🔧 Начало изготовления: {start_date.strftime('%d.%m.%Y')}"""

        # Создаем событие на весь период изготовления
        event = {
            'summary': f'🍪 Заказ #{order_number} - {customer_name}',
            'description': description,
            'start': {
                'date': start_date.strftime('%Y-%m-%d'),
                'timeZone': 'Europe/Madrid',  # Измените на ваш часовой пояс
            },
            'end': {
                'date': delivery_date.strftime('%Y-%m-%d'),
                'timeZone': 'Europe/Madrid',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},  # За день до выдачи
                    {'method': 'popup', 'minutes': 60},  # За час до выдачи
                ],
            },
            'colorId': '5',  # Желтый цвет (можно изменить 1-11)
        }

        try:
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()

            logger.info(f"Событие создано в Google Calendar: {event.get('htmlLink')}")
            return event.get('id')

        except HttpError as error:
            logger.error(f"Ошибка при создании события в календаре: {error}")
            return None

    def update_order_event(
        self,
        event_id: str,
        **kwargs
    ) -> bool:
        """
        Обновляет существующее событие в календаре

        Args:
            event_id: ID события в Google Calendar
            **kwargs: Параметры для обновления (те же что в create_order_event)

        Returns:
            True если успешно обновлено
        """
        if not self.service:
            if not self.authenticate():
                return False

        try:
            # Получаем существующее событие
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()

            # Обновляем поля (здесь можно добавить логику обновления)
            # event['summary'] = ...

            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event
            ).execute()

            logger.info(f"Событие обновлено: {updated_event.get('htmlLink')}")
            return True

        except HttpError as error:
            logger.error(f"Ошибка при обновлении события: {error}")
            return False

    def delete_order_event(self, event_id: str) -> bool:
        """
        Удаляет событие из календаря (при отмене заказа)

        Args:
            event_id: ID события в Google Calendar

        Returns:
            True если успешно удалено
        """
        if not self.service:
            if not self.authenticate():
                return False

        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()

            logger.info(f"Событие удалено из календаря: {event_id}")
            return True

        except HttpError as error:
            logger.error(f"Ошибка при удалении события: {error}")
            return False


# Глобальный экземпляр для использования в приложении
calendar_integration = GoogleCalendarIntegration()
