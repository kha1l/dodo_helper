from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from config.conf import Config
from postgres.psql import Database


async def authorization():
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './config/writer.json',
        scopes=scopes
    )
    gsc = gspread.authorize(credentials)
    return gsc


async def load():
    cfg = Config()
    db = Database()
    df_all = pd.read_json('https://publicapi.dodois.io/ru/api/v1/unitinfo/pizzerias')
    google_table = await authorization()
    gt = google_table.open_by_key(cfg.table).worksheet('Ответы на форму')
    df_worksheet = get_as_dataframe(gt)
    df_worksheet.drop([col for col in df_worksheet.columns if "Unnamed" in col], axis=1, inplace=True)
    df = df_worksheet.dropna(subset=['requestid'])
    users = db.get_name()
    all_rest = []
    for user in users:
        all_rest.append(user[0])
    for rest in df['pizzeriaName']:
        if rest in all_rest:
            continue
        else:
            df_rest = df.loc[df['pizzeriaName'] == rest]
            username = df_rest.iloc[0]['name']
            email = df_rest.iloc[0]['email']
            rest = df_rest.iloc[0]['pizzeriaName']
            login = df_rest.iloc[0]['login']
            password = df_rest.iloc[0]['password']
            code = df_rest.iloc[0]['country']
            request = df_rest.iloc[0]['requestid']
            df_rat = df_all.loc[df_all['Name'] == rest].reset_index()
            try:
                rest_id = int(df_rat.iloc[0]['Id'])
                long_id = df_rat.iloc[0]['UUId']
                status = 'work'
            except IndexError:
                rest_id, long_id = 0, '-'
                status = 'lose'
            db.add_settings(username, email, rest, login, password, code, request, status, rest_id, long_id)
