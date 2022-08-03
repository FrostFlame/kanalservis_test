import datetime
import json

import requests

from kanalservis.settings import BOT_TOKEN
from web.models import Order, Chat


def notify():
    """
    Скрипт отправки уведомлений об окончании срока поставки в Telegram.
    Бот - https://t.me/kanalservis07_test_bot
    Достаточно написать боту /start и вы будете добавлены в список
    рассылки
    """
    orders = Order.objects.filter(
        date=datetime.datetime.today() - datetime.timedelta(days=1)
    )
    if orders:
        msg = 'Сегодня прошёл срок поставки следующих заказов:\n'
        for order in orders:
            msg += f'Заказ № {order.order_number}, стоимость в $ ' \
                   f'{order.price_dol}$, стоимость в руб. ' \
                   f'{order.price_rub} руб., срок поставки ' \
                   f'{order.date}\n'

        chat_ids = get_updated_chat_ids()
        for chat_id in chat_ids:
            send_text = f'https://api.telegram.org/bot{BOT_TOKEN}/' \
                        f'sendMessage?chat_id={str(chat_id)}&parse_mode' \
                        f'=Markdown&text={msg}'

            requests.get(send_text)


def get_updated_chat_ids():
    """
    Обновление списка ролучателей уведомлений.
    """
    updates = json.loads(
        requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
        ).content
    )['result']
    for u in updates:
        try:
            Chat.objects.get_or_create(
                chat_id=u['message']['chat']['id']
            )
        except KeyError:
            pass
    return Chat.objects.values_list('chat_id', flat=True)