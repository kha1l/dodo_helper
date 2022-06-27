from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import get_as_dataframe
from postgres.psql import Database
import pandas as pd
from config.conf import Config


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
    google_table = await authorization()
    gt = google_table.open_by_key(cfg.table).worksheet('Ответы на форму')
    df_worksheet = get_as_dataframe(gt)
    df_worksheet.drop([col for col in df_worksheet.columns if "Unnamed" in col], axis=1, inplace=True)
    df = df_worksheet.dropna(subset=['requestid'])
    print(df)
