import datetime
import os

import requests
import xmltodict

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from web.models import Order

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1G-wfEmNeFqN4ztzFJpozYykCFoPClku44UHHHIk2eiQ'
SAMPLE_RANGE_NAME = 'A2:D'


def update_db():
    """Обновление базы данных."""
    print('start')
    creds = None
    if os.path.exists('web/updater/token.json'):
        creds = Credentials.from_authorized_user_file(
            'web/updater/token.json', SCOPES
        )
    if not creds or not creds.valid:
        """Получение и сохранение креденшелов"""
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'web/updater/credentials.json', SCOPES
            )
            creds = flow.run_local_server()
        with open('web/updater/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        """Обращение к таблице"""
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME
        ).execute()
        values = result.get('values', [])

        ids = []
        for row in values:
            if not row:
                continue
            ids.append(row[0])
            dollar_value = None
            order_date = row[3]
            while dollar_value is None:
                """
                Для некоторых дат нет значений курса доллара, цикл
                отсчитывает до ближайшего предыдущего дня, для
                которого курс доллара задан
                """
                if type(order_date) == datetime.datetime:
                    order_date = order_date.strftime('%d.%m.%Y')
                dollar_value = requests.get(
                    'http://www.cbr.ru/scripts/XML_dynamic.asp',
                    params={'date_req1': order_date,
                            'date_req2': order_date,
                            'VAL_NM_RQ': 'R01235'
                            }
                )
                try:
                    dollar_value = float(
                        xmltodict.parse(
                            dollar_value.content
                        )['ValCurs']['Record']['Value'].replace(',', '.')
                    )
                except KeyError:
                    dollar_value = None
                    order_date = datetime.datetime.strptime(
                        order_date, '%d.%m.%Y'
                    ) - datetime.timedelta(days=1)
            Order.objects.update_or_create(
                id=row[0], defaults={
                    'price_rub': float(
                        row[2].replace(',', '.')
                    ) * dollar_value,
                    'price_dol': row[2],
                    'date': datetime.datetime.strptime(
                        row[3], '%d.%m.%Y'
                    ).date(),
                    'order_number': row[1]},)
        Order.objects.exclude(id__in=ids).delete()
    except HttpError as err:
        print(err)
