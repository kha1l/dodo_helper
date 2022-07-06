from postgres.psql import Database
from datetime import datetime, timedelta


async def change_time(date):
    try:
        avg = str(date).split(' ')[2]
    except IndexError:
        avg = str(date)
    hms = avg.split(':')
    if int(hms[0]) != 0:
        return f'{int(hms[0])} ч. {int(hms[1])} мин.'
    else:
        return f'{int(hms[1])} мин.'


async def get_list_prom(chat_id):
    db = Database()
    text = db.select_prom(chat_id)
    message = ''
    for i in text:
        if i[1] == 'orders':
            message += f'{i[0]} - отчеты по курьерам\n'
        elif i[1] == 'happy':
            message += f'{i[0]} - дни рождения\n'
        elif i[1] == 'metrics':
            message += f'{i[0]} - метрики\n'
    return message


async def delete_prom(chat):
    db = Database()
    db.delete_prom(chat)


async def get_wait(date, rest):
    db = Database()
    row_wait = db.select_row_on_wait(date, rest)
    message = f'{rest} за {date}:\n Ожидания:\n'
    for j in row_wait:
        user = j[0]
        order = j[1]
        meat = (str(j[2]).split(' '))[1]
        queue = (str(j[3]).split(' '))[1]
        delivery = (str(j[4]).split(' '))[1]
        total = j[5]
        message += f'  {user} - {order} заказ:\n   готов: {meat};\n' \
                   f'   в очереди: {queue};\n   время отъезда: {delivery};\n' \
                   f'   заказов в поездке: {total}.\n\n'
    return message


async def get_pause(date, rest):
    db = Database()
    row_pause = db.select_row_on_pause(date, rest)
    message = f'\n Паузы:\n'
    for i in row_pause:
        user = i[0]
        begin = (str(i[1]).split(' '))[1]
        duration = i[2]
        message += f'  курьер: {user};\n  начало: {begin};\n  длительность: {duration}.\n\n'
    return message


async def get_later(date, rest):
    db = Database()
    row_later = db.select_row_on_later(date, rest)
    message = '\n Опоздания:\n'
    for i in row_later:
        user = i[0]
        duration = await change_time(i[1])
        message += f'  {user}\n  опоздал(а) на {duration}\n\n'
    return message


async def get_over(date, rest):
    db = Database()
    n_date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d') - timedelta(days=6), '%Y-%m-%d')
    row_over = db.select_row_on_over(date, n_date, rest)
    message1 = f'\n Не выход на смену:\n'
    message2 = f'\n Выход не в свою смену:\n'
    for i in row_over:
        user = i[0]
        if i[1] == 1:
            message1 += f'{i[2]} {user} не вышел на смену.\n\n'
        else:
            message2 += f'{i[2]} {user} вышел не в свою смену.\n\n'
    return message1 + message2


