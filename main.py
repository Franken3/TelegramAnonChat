import asyncio
import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from functions import add_in_search, check_not_in_search, check_user_in_chat, \
    registration, get_companion_chat_id, stop_chat, del_from_search, \
    get_companin_username, search, reg_age_sex

TOKEN = "1945086696:AAGeOn29Jhc8cECb8NgS7u3PQ_Ahzomh-eo"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    sex = State()  # Will be represented in storage as 'Form:sex'
    age = State()  # Will be represented in storage as 'Form:age'
    companion = State()
    in_search = State()

class Queue:
    inSearch = []
    def __init__(self):
        pass
    def add_in_search(self, user, chat_id):
        self.inSearch.append({user:chat_id})

queue = Queue()


button_next = KeyboardButton('/next')
button_stop = KeyboardButton('/stop')

bt_female = KeyboardButton('Девушка')
bt_male = KeyboardButton('Парень')

keyboard = ReplyKeyboardMarkup()


@dp.message_handler(commands=['start'])
async def start(message):
    username = message.from_user.username

    await bot.send_message(message.chat.id, f'<b><i>Добро пожаловать в чат, {message.from_user.first_name}</i></b>',
                           parse_mode='html')
    await asyncio.sleep(0.5)
    await bot.send_message(message.chat.id, '<i>Напишите</i> /search <i>для начала диалога</i>', parse_mode='html')
    registration(username, message.chat.id)
    print(f'{username} new user')


@dp.message_handler(commands=['reg'])
async def registr(message):
    username = message.from_user.username
    #await bot.send_message()
    await Form.sex.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(bt_male, bt_female)
    await bot.send_message(message.chat.id, 'Для регистарации укажите ваш пол', reply_markup=keyboard)


@dp.message_handler(state=Form.sex)
async def sex_reg(message, state: FSMContext):
    async with state.proxy() as data:
        data['sex'] = message.text
    await Form.next()
    await bot.send_message(message.chat.id, "Укажите ваш возраст", reply_markup= types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.age)
async def age_reg(message, state: FSMContext):
    username = message.from_user.username
    if message.text.isdigit():
        async with state.proxy() as data:
            data['age'] = message.text
            reg_age_sex(username, data['age'], data['sex'])
            print(data)
        await bot.send_message(message.chat.id, f'Ваш пол: {data["sex"]}\n'
                                                f'Ваш возраст: {data["age"]}')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Укажите возраст написав число')


@dp.message_handler(commands=['search', 'next'])
async def start_search(message):
    username = message.from_user.username
    if check_not_in_search(username):
        await bot.send_message(message.chat.id, 'Ищем вам собеседника \n\n' +
                               '<i>Напишите</i> /stop <i>для остановки поиска</i>', parse_mode='html')
        add_in_search(username)

        count = 0
        while not check_not_in_search(username):
            count += 1
            search(username)
            if count % 10 == 0:
                await bot.send_message(message.chat.id, 'Продолжаю поиск', parse_mode='html')
            await asyncio.sleep(1)
        if check_user_in_chat(username):
            await bot.send_message(message.chat.id, 'Собеседник найден \n\n' +
                                   '/next Для поиска нового собеседника\n\n' +
                                   '<i>Напишите</i> /stop <i>для остановки диалога</i>', parse_mode='html')
    else:
        await bot.send_message(message.chat.id, 'Уже ищем вам собеседника \n\n' +
                               '<i>Напишите</i> /stop <i>для остановки поиска</i>', parse_mode='html')


@dp.message_handler(commands=['stop'])
async def stop(message):
    username = message.from_user.username
    if check_user_in_chat(username):
        await bot.send_message(message.chat.id, 'Чат остановлен \n\n' +
                               '<i>Напишите</i> /next <i>для поиска нового собеседника</i>', parse_mode='html')
        await bot.send_message(get_companion_chat_id(username), 'Собеседник закончил диалог с вами\n\n' +
                               '<i>Напишите</i> /next <i>для поиска нового собеседника</i>', parse_mode='html')
        stop_chat(username)
        stop_chat(get_companin_username(username))
    elif not check_not_in_search(username):
        del_from_search(username)
        await bot.send_message(message.chat.id, 'Поиск отановлен \n\n' +
                               '<i>Напишите</i> /next <i>для поиска нового собеседника</i>', parse_mode='html')
    else:
        await bot.send_message(message.chat.id, 'Вы не в чате или не ищите собеседника \n\n' +
                               '<i>Напишите</i> /next <i>для поиска нового собеседника</i>', parse_mode='html')


@dp.message_handler(content_types=['text', 'photo', 'sticker', 'voice', 'video', 'document'])
async def tet_a_tet(message, state: FSMContext):
    username = message.from_user.username
    # print(message.reply_to_message.message_id)
    # await bot.send_message(message.chat.id,text='sd',reply_to_message_id=1)
    if check_user_in_chat(username):

        if 'text' in message:
            await bot.send_message(get_companion_chat_id(username), message.text)

        elif 'sticker' in message:
            await bot.send_sticker(get_companion_chat_id(username), message.sticker.file_id)

        elif 'photo' in message:
            file_unique_id = message.photo[-1].file_unique_id
            await message.photo[-1].download(f'photos/{file_unique_id}.jpg')
            photo = open(f'photos/{file_unique_id}.jpg', 'rb')
            await bot.send_photo(get_companion_chat_id(username), photo)
            os.remove(f'photos/{file_unique_id}.jpg')

        elif 'voice' in message:
            file_unique_id = message.voice.file_unique_id
            await message.voice.download(f'voices/{file_unique_id}.ogg')
            voice = open(f'voices/{file_unique_id}.ogg', 'rb')
            await bot.send_voice(get_companion_chat_id(username), voice)
            os.remove(f'voices/{file_unique_id}.ogg')

        elif 'video' in message:
            file_unique_id = message.video.file_unique_id
            await message.video.download(f'videos/{file_unique_id}.mp4')
            video = open(f'videos/{file_unique_id}.mp4', 'rb')
            await bot.send_video(get_companion_chat_id(username), video)
            os.remove(f'videos/{file_unique_id}.mp4')


        elif 'document' in message:
            await bot.send_message(message.chat.id, '<b>Бот не отправляет файлы!</b>\n'
                                                    '\nОтправтье фото или видео')
        #    file_unique_id = message.document.file_unique_id
        #    await message.document.download(f'documents/{file_unique_id}')
        #    document = open(f'documents/{file_unique_id}', 'rb')
        #    os.remove(f'documents/{file_unique_id}')

    else:
        await bot.send_message(message.chat.id, 'Вы не в чате \n\n' +
                               '<i>Напишите</i> /next <i>для поиска нового собеседника</i>', parse_mode='html')

if __name__ == '__main__':
    executor.start_polling(dp)
