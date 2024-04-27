from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pg_maker import all_authors, find_author
from utils.calendar import current_month, current_day, next_month
from collections import defaultdict
import os


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "14rfetnaiqgiT3o0TsLC-yi3EICobIH5rNljilhDS70M"

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

def get_data_from_sheet(month):
    SAMPLE_RANGE_NAME = f"{month}!A2:I"

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
            print("No data found.")
            return None

        return values

    except HttpError as err:
        print(err)
        return None


def rep_month(month):
    values = get_data_from_sheet(month)
    if not values:
        return

    dct = dict()

    for row in values:
      try:
        key = row[2]
        value = int(row[6])
        if key in dct:
          current_sum, current_count = dct[key]
          dct[key] = (current_sum + value, current_count + 1)
        else:
          dct[key] = (value, 1)
      except:
        pass

    msg = ''
    sorted_dct = sorted(dct.items(), key=lambda item: item[1][0], reverse=True)
    for author, summa in sorted_dct:
        msg += f"{author} — {summa[0]} руб.\nТекстов за месяц — {summa[1]}\n\n"
    return msg


def rep_name_and_month(name, month='Январь 2024'):
    values = get_data_from_sheet(month)
    if not values:
        return

    dct = dict()
    dct_texts = dict()
    texts_in_work = dict()
    texts_in_work[name] = []
    for row in values:
        try:
            title = f"{row[0]} — {row[6]} руб. {row[1]}"
            money = int(row[6])
            link = row[1]
            brief = str(row[3])
            if name == row[2]:
                if (name in dct or name in dct_texts):
                    if link:
                        value_money, current_count = dct[name]
                        dct_texts[name].append(title)
                        dct[name] = (value_money + money, current_count + 1)
                    else:
                        texts_in_work[name].append((title, brief))
                else:
                    dct[name] = (money, 1)
                    dct_texts[name] = [title]
        except:
            pass
    msg = ''
    sorted_dct = sorted(dct.items(), key=lambda item: item[1][0], reverse=True)
    for author, summa in sorted_dct:
        msg += f"Гонорар за сданные тексты за {month} — {summa[0]} руб.\nТекстов за месяц — {summa[1]}\n\n"

    msg_texts = '<b>Все сданные тексты:</b> \n'
    for title in dct_texts[name]:
        msg_texts += f"\n— {title}\n"
    msg += msg_texts

    msg_texts_in_work = '\n\n<b>Тексты в работе: </b>\n'
    for title in texts_in_work[name]:
        msg_texts_in_work += f"\n— <a href='{title[1]}'>{title[0]}</a>\n"
    msg += msg_texts_in_work
    return msg


def who_is_free():
    values = get_data_from_sheet(current_month())
    if not values:
        return

    all_nicknames = [(i[1], i[2]) for i in all_authors()]
    all_nicknames_2 = [(i[1], i[2]) for i in all_authors()]
    count_dict = defaultdict(int)
    for row in values:
        try:
            author = str(row[2])
            link = row[1]
            if author and not link:
                count_dict[author] += 1
                for nickname_tuple in all_nicknames:
                    if author in nickname_tuple:
                        all_nicknames.remove(nickname_tuple)
        except:
            pass

    result = [author for author, count in count_dict.items() if count == 1]

    nicknames_2 = [nickname for nickname in all_nicknames_2 if any(author in nickname for author in result)]

    return all_nicknames, nicknames_2


def brief_is_free():
    now_and_next_month = [current_month(), next_month()]
    all_briefs = []
    for month in now_and_next_month:
        values = get_data_from_sheet(month)
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


def stats_for_month(month):
    values = get_data_from_sheet(month)
    if not values:
        return

    done, in_work, all_texts, seo, simple, review, test = 0, 0, 0, 0, 0, 0, 0
    deadline_today = ''
    for row in values:
        try:
            title = row[0]
            link = row[1]
            brief = row[3]
            type = row[5]
            deadline = row[7]
            author = row[2]

            seo += 1 if type == 'СЕО' else 0
            simple += 1 if type == 'Простая' or row[5] == 'Новость' else 0
            review += 1 if type == 'Обзор' else 0
            test += 1 if type == 'Тест' else 0

            if title and brief:
                all_texts += 1

                if link:
                    done += 1
                else:
                    in_work += 1

            if deadline and title and brief:
                deadline_today += f"{title} — {author} — {deadline}\n"
        except:
            pass

    msg = f'Всего текстов за месяц: {all_texts}\n' \
          f'Уже готовы: {done}\n' \
          f'Сейчас в работе: {in_work}\n\n' \
          f'Простых — {simple} шт\n' \
          f'СЕО — {seo} шт\n' \
          f'Тестов — {test}\n' \
          f'Обзоров — {review}\n\n\n'
    return msg


def in_work_today():
    values = get_data_from_sheet(current_month())
    if not values:
        return
    today, tomorrow = current_day()

    done, in_work, all_texts = 0, 0, 0
    deadline_today = ''
    deadline_tomorrow = ''
    for row in values:
        try:
            title = row[0]
            link = row[1]
            brief = row[3]
            deadline = row[7]
            author = row[2]

            if title and brief and title != "Тема текста" and title != "МВИДЕО":
                all_texts += 1

                if link:
                    done += 1
                else:
                    in_work += 1

            if deadline and title and brief and not link:
                if deadline == today:
                    deadline_today += f"- <a href='{brief}'>{title}</a> — {author} {find_author(author)[0]}\n\n"
                if deadline == tomorrow:
                    deadline_tomorrow += f"- <a href='{brief}'>{title}</a> — {author} {find_author(author)[0]}\n\n"
        except:
            pass

    msg = f'Всего текстов за месяц: {all_texts}\n' \
          f'Уже готовы: {done}\n' \
          f'Сейчас в работе: {in_work}\n\n' \
          f'<b>Сегодня должны сдать:</b> \n{deadline_today}\n\n' \
          f'<b>Завтра должны сдать:</b> \n{deadline_tomorrow}\n\n'
    return msg


def all_texts_of_author(name):
    all_months = get_sheet_names()
    temp_eldo = ""
    temp_mvideo = ""
    recording_mvideo = False

    for month in all_months:
        values = get_data_from_sheet(month)
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
                if name == row[2] and link:
                    if recording_mvideo:
                        msg_texts_mvideo += f"\n{title}\n"
                    else:
                        msg_texts_eldo += f"\n{title}\n"
            except:
                pass

        temp_eldo += msg_texts_eldo
        temp_mvideo += msg_texts_mvideo

        recording_mvideo = False

    temp_file_eldo = create_and_return_file(name, 'eldo', temp_eldo)
    temp_file_mvideo = create_and_return_file(name, 'mvideo', temp_mvideo)

    return temp_file_eldo, temp_file_mvideo


def create_and_return_file(name, blog, content):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    temp_directory = os.path.join(current_directory, "report_bot", "temp")
    os.makedirs(temp_directory, exist_ok=True)
    file_path = os.path.join(temp_directory, f"{name}_{blog}.txt")
    with open(file_path, "a") as file:
        if content:
            file.write(content)
            return file_path
        else:
            return ''








