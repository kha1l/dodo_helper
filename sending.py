from aiogram.utils.exceptions import MessageIsTooLong, BotBlocked
from datetime import datetime, timedelta
from works import get_wait, get_over, get_later, get_pause
from postgres.psql import Database
from config.conf import Config


# Сбор и отправка данных о днях рождениях персонала
async def send_birthday():
    db = Database()
    cfg = Config()
    emoji = u'\U0001F389'
    base = db.select_all_user_on_groups(post='happy')
    for j in base:
        rest = j[0]
        data = db.select_birthday(rest)
        for i in data:
            text = f'{emoji} {rest}: {i[0]} {i[1]} {i[2]}'
            try:
                await cfg.bot.send_message(j[1], text)
            except BotBlocked:
                pass


# Сбор и отправка данных статистики курьеров
async def send_mess_stats():
    db = Database()
    cfg = Config()
    base = db.select_all_user_on_groups(post='orders')
    date = str((datetime.now() - timedelta(days=1)).date())
    for i in base:
        rest = i[0]
        # Вызов функции для нахождения
        message = await get_wait(date, rest) + await get_pause(date, rest) + await get_later(date, rest)
        try:
            await cfg.bot.send_message(i[1], message)
        except MessageIsTooLong:
            for x in range(0, len(message), 4096):
                await cfg.bot.send_message(i[1], message[x:x + 4096])
        except BotBlocked:
            pass


async def send_mess_week_stats():
    db = Database()
    cfg = Config()
    base = db.select_all_user_on_groups(post='orders')
    date = str((datetime.now() - timedelta(days=1)).date())
    for i in base:
        rest = i[0]
        message = await get_over(date, rest)
        try:
            await cfg.bot.send_message(i[1], message)
        except MessageIsTooLong:
            for x in range(0, len(message), 4096):
                await cfg.bot.send_message(i[1], message[x:x + 4096])
        except BotBlocked:
            pass


async def send_mess_metrics():
    db = Database()
    cfg = Config()
    base = db.select_all_user_on_groups(post='metrics')
    for i in base:
        rest = i[0]
        data = db.select_metrics(rest)
        try:
            text = f'Метрики на {data[0]} в пиццерии {rest}:\nВыручка     - {data[1]};' \
                   f'\nПроизвод.   - {data[2]};\nПрод./час   - {data[3]};\nКур./час     - {data[4]};' \
                   f'\nДоставка   - {data[5]};\nСертики    - {data[6]}.'
            try:
                await cfg.bot.send_message(i[1], text)
            except BotBlocked:
                pass
        except TypeError:
            pass
