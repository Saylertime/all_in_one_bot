from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as CREDS
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.calend import current_month
import os
import gspread


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1OkXB-077V0WEO8TbZOfgcBbsh-wVGhtTRrW__p3NY0U"

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

def get_sheet_names():
    try:
        service = build("sheets", "v4", credentials=creds)

        spreadsheet = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        sheets = spreadsheet.get('sheets', [])

        sheet_names = [sheet['properties']['title'] for sheet in sheets]
        return sheet_names

    except HttpError as err:
        print(err)
        return None

def get_data_from_sheet(username):
    SAMPLE_RANGE_NAME = "АВТОРЫ!A2:I"

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            return None
        for value in values:
            if username in value:
                return value[0]

    except HttpError as err:
        print(err)
        return None


def new_list(username, msg):

    SERVICE_ACCOUNT_FILE = 'noted-aloe-312816-1a7fb3d4ab15.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = CREDS.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    new_sheet_name = str(current_month())

    try:
        spreadsheet.add_worksheet(title=new_sheet_name, rows=100, cols=20)
        print(f'Создан новый лист "{new_sheet_name}')
    except:
        print('Лист уже создан?..')

    try:
        sheet = spreadsheet.worksheet(new_sheet_name)
        cell = sheet.find(username)
        if cell:
            row_number = cell.row
            sheet.update_cell(row_number, 2, msg)
            print(f'Обновлено сообщение для пользователя {username}')
        else:
            row = [username, msg]
            sheet.append_row(row)
            print(f'Добавлена строка для пользователя {username}')
    except gspread.exceptions.APIError as e:
        print(f'Произошла ошибка: {e}')
