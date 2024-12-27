from gspread_asyncio import AsyncioGspreadClientManager
from google.oauth2.service_account import Credentials as ServiceAccountCredentials

import os
from utils.calend import current_month


SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "noted-aloe-312816-1a7fb3d4ab15.json"
SAMPLE_SPREADSHEET_ID = "1OkXB-077V0WEO8TbZOfgcBbsh-wVGhtTRrW__p3NY0U"
SAMPLE_RANGE_NAME = "A2:I"


def get_gspread_client_manager():
    credentials = ServiceAccountCredentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return AsyncioGspreadClientManager(lambda: credentials)


async def get_sheet_names():
    """Получает названия всех листов в таблице."""
    client_manager = get_gspread_client_manager()
    client = await client_manager.authorize()  # Асинхронно получаем клиента
    try:
        spreadsheet = await client.open_by_key(SAMPLE_SPREADSHEET_ID)
        sheets = await spreadsheet.fetch_sheet_metadata()
        sheet_names = [sheet["properties"]["title"] for sheet in sheets.get("sheets", [])]
        return sheet_names
    except Exception as err:
        print(f"Ошибка при получении имен листов: {err}")
        return None



async def get_data_from_sheet(username):
    """Получает данные из таблицы по имени пользователя."""
    client_manager = get_gspread_client_manager()
    client = await client_manager.authorize()  # Асинхронно получаем клиента
    try:
        spreadsheet = await client.open_by_key(SAMPLE_SPREADSHEET_ID)
        worksheet = await spreadsheet.worksheet("АВТОРЫ")
        values = await worksheet.get(SAMPLE_RANGE_NAME)

        if not values:
            return None

        for value in values:
            if username in value:
                return value[0]
    except Exception as err:
        print(f"Ошибка при получении данных из таблицы: {err}")
        return None


async def new_list(username, msg):
    """Создает новый лист или обновляет существующий."""
    client_manager = get_gspread_client_manager()
    client = await client_manager.authorize()  # Асинхронно получаем клиента
    try:
        spreadsheet = await client.open_by_key(SAMPLE_SPREADSHEET_ID)
        new_sheet_name = str(current_month())

        try:
            await spreadsheet.add_worksheet(title=new_sheet_name, rows=100, cols=20)
            print(f'Создан новый лист "{new_sheet_name}"')
        except Exception:
            print("Лист уже создан?..")

        worksheet = await spreadsheet.worksheet(new_sheet_name)
        cell = await worksheet.find(username)

        if cell:
            row_number = cell.row
            await worksheet.update_cell(row_number, 2, msg)
            print(f"Обновлено сообщение для пользователя {username}")
        else:
            row = [username, msg]
            await worksheet.append_row(row)
            print(f"Добавлена строка для пользователя {username}")

    except Exception as err:
        print(f"Произошла ошибка: {err}")
