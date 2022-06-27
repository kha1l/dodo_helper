from aiogram import executor, types
from config.conf import Config, States
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from postgres.psql import Database
from keyboard.key import Keyboard
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from updater.loads import load


cfg = Config()
db = Database()
key = Keyboard()


@cfg.dp.message_handler(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}! \U0001F44B\n', reply_markup=key.choice)
    await States.choice.set()


@cfg.dp.callback_query_handler(text='continue', state=States.choice)
async def checking(call: types.CallbackQuery):
    await call.message.answer(f'Введите название ресторана для проверки авторизации.\n'
                              f'Например: Петергоф-1\n')
    await States.choice_pizza.set()


@cfg.dp.callback_query_handler(text='update', state=States.choice)
async def checking(call: types.CallbackQuery):
    await call.answer(f'Данные обновляются...')
    await load()


@cfg.dp.callback_query_handler(text='back', state=States.choice)
async def checking(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Good luck!')
    await state.finish()


@cfg.dp.message_handler(state=States.choice_pizza)
async def check_rest(message: types.Message, state: FSMContext):
    rest = db.check_rest(message.text)
    if rest is None:
        await message.answer(f'Ссылка на авторизацию - https://uk-vkus.ru/form-dodohelper\n'
                             f'1.Логин должен начинаться с "ddb_".\n'
                             f'  Например: ddb_petergof\n'
                             f'2.Пароль(пример): Fps324sq\n'
                             f'3.Учетная запись только для Менеджера Офиса\n'
                             f'4.Для разных городов, разные учётные записи.\n'
                             f'  Допускается в одной например: Петергоф-1,\n'
                             f'  Петергоф-2, Петергоф-3 и тд.\n'
                             f'5.Убедитесь что логин и пароль введены корректно.\n'
                             f'6.Обновите данные нажав на соответствующую кнопку.\n')
        await state.finish()
    else:
        await state.update_data(name=message.text)
        await message.answer(f'\U0001F4A1 Выбери то, что тебя интересует!', reply_markup=key.post)
        await States.choice_post.set()


@cfg.dp.callback_query_handler(text='over', state=States.choice_post)
async def exit_post(call: types.CallbackQuery):
    await call.message.answer('Подписаться еще на один ресторан или выйти.', reply_markup=key.choice)
    await States.choice.set()


@cfg.dp.callback_query_handler(text='exit', state=States.choice_post)
async def exit_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await cfg.bot.send_message(call.message.chat.id, text=f'\U0000270B До свидания!')
    await state.finish()


@cfg.dp.callback_query_handler(key.set_callback1.filter(), state=States.choice_post)
async def show_rest(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    chat = call.message.chat.id
    await state.update_data(chat_id=chat, post=callback_data.get('func_id'))
    callback = await state.get_data()
    try:
        db.add_client(callback['name'], callback['chat_id'], callback['post'])
        await call.message.answer(f'\U00002705 Вы подписались на отчет!')
    except errors.lookup(UNIQUE_VIOLATION):
        await call.message.answer(f'\U000026A0 Вы уже подписаны на данный отчет!')


if __name__ == '__main__':
    executor.start_polling(cfg.dp)
