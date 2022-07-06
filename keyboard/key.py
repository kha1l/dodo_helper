from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Keyboard:
    set_callback1 = CallbackData('s', 'func_id')

    choice = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Проверить пиццерию',
                callback_data='continue'
            )],
        [
            InlineKeyboardButton(
                text=f'Обновить данные',
                callback_data='update'
            )],
        [
            InlineKeyboardButton(
                text=f'Выход',
                callback_data='back'
            )]
    ])

    post = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Отчеты по курьерам',
                callback_data=set_callback1.new(func_id='orders')
            )],
        [
            InlineKeyboardButton(
                text=f'Дни рождения сотрудников',
                callback_data=set_callback1.new(func_id='happy')
            )],
        [
            InlineKeyboardButton(
                text=f'Метрики',
                callback_data=set_callback1.new(func_id='metrics')
            )],
        [
            InlineKeyboardButton(
                text=f'Сертификаты',
                callback_data=set_callback1.new(func_id='cert')
            )],
        [
            InlineKeyboardButton(
                text=f'Назад к выбору пиццерии',
                callback_data='over'
            )],
        [
            InlineKeyboardButton(
                text=f'Закончить работу',
                callback_data='exit'
            )]
    ])
