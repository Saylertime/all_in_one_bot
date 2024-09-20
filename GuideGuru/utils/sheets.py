from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.calend import current_month, next_month
import os


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID_ELDO = "14rfetnaiqgiT3o0TsLC-yi3EICobIH5rNljilhDS70M"
SAMPLE_SPREADSHEET_ID_SBER = "1TimmvVzxIn5J_1HeXpjuf0PIGq-gdLb6Yr4r7enEImo"


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


def get_sheet_names(spreadsheet_id):
    try:
        service = build("sheets", "v4", credentials=creds)

        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet.get('sheets', [])

        sheet_names = [sheet['properties']['title'] for sheet in sheets]
        return sheet_names

    except HttpError as err:
        print(err)
        return None


def get_data_from_sheet(month, spreadsheet_id):
    SAMPLE_RANGE_NAME = f"{month}!A2:M"

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return None

        return values

    except HttpError as err:
        print(err)
        return None


def rep_name_and_month(name, month=current_month(), sber_data=None):
    print(sber_data)
    values = get_data_from_sheet(month, SAMPLE_SPREADSHEET_ID_ELDO)
    name = name[0]
    if not values:
        return
    try:
        dct = dict()
        dct_texts = dict()
        texts_in_work = dict()
        texts_in_work[name] = []
        dict_with_addons = {}

        if sber_data:
            dct.update(sber_data['dct'])
            dct_texts.update(sber_data['dct_texts'])
            texts_in_work[name].extend(sber_data['texts_in_work'].get(name, []))

        for row in values:
            try:
                title = f"\n— <a href='{row[1]}'>{row[0]}</a> — {row[6]} руб.\n"
                money = int(row[6])
                link = row[1]
                brief = str(row[3])
                try:
                    bonus_pts = int(row[9])
                except:
                    bonus_pts = 1

                if name == row[2]:
                    if name in dct:
                        value_money, current_count, general_bonus = dct[name]
                        if link:
                            dct_texts[name].append(title)
                            current_count += 1
                            general_bonus += bonus_pts
                            dct[name] = (value_money + money, current_count, general_bonus)
                        else:
                            texts_in_work[name].append((title, brief))
                    else:
                        dct[name] = (money, 1, bonus_pts)
                        dct_texts[name] = [title]
            except Exception as e:
                print(f"Error processing row: {e}")
                pass

        for row in values:
            try:
                if name == row[10]:
                    money = int(row[11])
                    addons = str(row[12])

                    if name in dict_with_addons:
                        dict_with_addons[name].append((money, addons))
                    else:
                        dict_with_addons[name] = [(money, addons)]

                    if name in dct:
                        value_money, current_count, general_bonus = dct[name]
                        general_bonus += 1
                        dct[name] = (value_money + money, current_count, general_bonus)
                    else:
                        dct[name] = (money, 0, 0)
            except:
                pass

        msg = ''
        sorted_dct = sorted(dct.items(), key=lambda item: (item[1][0], item[1][2]), reverse=True)
        bonus_money = 0
        for author, (summa, count, general_bonus) in sorted_dct:
            if general_bonus >= 20:
                bonus_money = 4000
            elif general_bonus >= 15:
                bonus_money = 2500
            elif general_bonus >= 10:
                bonus_money = 1500
            elif general_bonus >= 5:
                bonus_money = 500

            if author == 'Седна':
                summa += 60000

            total_money = sum(money for money, _ in dict_with_addons.get(name, []))

            msg += (f"Гонорар за сданные тексты и допы за {month} — {summa + bonus_money}  руб.\n"
                    f"Из них бонус — {bonus_money} руб.\n"
                    f"И допы — {total_money} руб.\n"
                    f"Всего бонусов набрано — {general_bonus} шт.\n"
                    f"Текстов за месяц — {count}.\n\n")

        msg_texts = '<b>Все сданные тексты:</b> \n'
        for title in dct_texts[name]:
            msg_texts += title
        msg += msg_texts

        if texts_in_work[name]:
            msg_texts_in_work = '\n\n<b>Тексты в работе:</b>'
            for title in texts_in_work[name]:
                msg_texts_in_work += f"\n<a href='{title[1]}'>{title[0]}</a>"
            msg += msg_texts_in_work

        if dict_with_addons:
            msg_addons = '\n\n<b>Дополнительные гонорары: </b>\n'
            for addon in dict_with_addons[name]:
                msg_addons += f"\n — {addon[1]} — {addon[0]} руб.\n"
            msg += msg_addons

        if len(msg) > 4090:
            msg_file = create_and_return_file(name, 'last_month', msg)
            return msg_file
        else:
            return msg

    except Exception as e:
        msg = f'Кажется, у тебя пока ничего не написано...'
        # msg = str(e)
        return msg


def rep_name_and_month_sber(name, month=current_month()):
    values = get_data_from_sheet(month, SAMPLE_SPREADSHEET_ID_SBER)
    name = name[0]
    if not values:
        return

    dct = dict()
    dct_texts = dict()
    texts_in_work = dict()
    texts_in_work[name] = []
    for row in values:
        try:
            title = f"\n— <a href='{row[1]}'>{row[0]}</a> — {row[3]} руб.\n"
            money = int(row[3])
            link = row[1]
            brief = str(row[4])
            general_bonus = 1

            if name == str(row[2]):
                if name in dct:
                    value_money, current_count, general_bonus = dct[name]
                    if link:
                        dct_texts[name].append(title)
                        current_count += 1
                        general_bonus += 1
                        dct[name] = (value_money + money, current_count, general_bonus)
                    else:
                        texts_in_work[name].append((title, brief))
                else:
                    dct[name] = (money, 1, general_bonus)
                    dct_texts[name] = [title]
        except Exception as e:
            print(f"Error processing row: {e}")
            pass

    return {
        'dct': dct,
        'dct_texts': dct_texts,
        'texts_in_work': texts_in_work
    }


def all_texts_of_author(name_in_db):

    all_months = get_sheet_names(SAMPLE_SPREADSHEET_ID_ELDO)
    temp_eldo = ""
    temp_mvideo = ""
    recording_mvideo = False

    for month in all_months:
        values = get_data_from_sheet(month, SAMPLE_SPREADSHEET_ID_ELDO)
        if not values:
            return

        msg_texts_eldo = ''
        msg_texts_mvideo = ''
        for row in values:
            if 'МВИДЕО' in str(row):
                recording_mvideo = True
            try:
                title = f"{row[0]} — {row[1]}"
                link = row[1]
                if name_in_db == row[2] and link:
                    if recording_mvideo:
                        msg_texts_mvideo += f"\n{title}\n"
                    else:
                        msg_texts_eldo += f"\n{title}\n"
            except:
                pass

        temp_eldo += msg_texts_eldo
        temp_mvideo += msg_texts_mvideo

        recording_mvideo = False

    temp_file_eldo = create_and_return_file(name_in_db, 'eldo', temp_eldo)
    temp_file_mvideo = create_and_return_file(name_in_db, 'mvideo', temp_mvideo)

    temp_eldo = ''
    temp_mvideo = ''

    return temp_file_eldo, temp_file_mvideo


def create_and_return_file(name, blog, content):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    temp_directory = os.path.join(current_directory, "temp")
    os.makedirs(temp_directory, exist_ok=True)
    file_path = os.path.join(temp_directory, f"{name}_{blog}.txt")
    with open(file_path, "w") as file:
        if content:
            file.write(content)
            return file_path
        else:
            return ''


def brief_is_free():
    now_and_next_month = [current_month(), next_month()]
    all_briefs = []
    for month in now_and_next_month:
        values = get_data_from_sheet(month, SAMPLE_SPREADSHEET_ID_ELDO)
        if not values:
            return

        flag_mvideo = False

        for row in values:
            if "МВИДЕО" in str(row):
                flag_mvideo = True
            try:
                title = str(row[0])
                brief = str(row[3])
                author = row[2]
                money = str(row[6])
                symbs = str(row[8])

                if brief and not author:
                    temp_row = f'[{title}]({brief})\n' \
                               f'Объем: {symbs} тыс. символов\n' \
                               f'Для блога: {"Мвидео" if flag_mvideo else "Эльдорадо"}\n' \
                               f'Гонорар: {money}\n\n'
                    all_briefs.append(temp_row)

            except Exception as e:
                print(f"Error: {e}")

    msg = ''
    for num, brief in enumerate(all_briefs, start=1):
        msg += f"{num}. {brief}"

    return msg

