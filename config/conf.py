from dotenv import load_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State


class Config:
    load_dotenv()
    dbase = os.getenv('DATA_BASE')
    user = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')
    host = os.getenv('IP')
    token = os.getenv('TOKEN')
    table = os.getenv('TABLE')
    bot = Bot(token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())


class States(StatesGroup):
    choice_pizza = State()
    choice_post = State()
    choice = State()
