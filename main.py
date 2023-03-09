import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv

from api import GPTApi

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


class ImagesForm(StatesGroup):
    text = State()


class CodeForm(StatesGroup):
    text = State()


m_img = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).row(KeyboardButton('Картинки'), KeyboardButton('Код'))


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Привет!", reply_markup=m_img)


@dp.message_handler(text="Картинки")
async def start(message: Message):
    await message.answer("Введите любое сообщение", reply_markup=m_img)
    await ImagesForm.text.set()


@dp.message_handler(state=ImagesForm.text)
async def images_cmd(message: Message, state: FSMContext):
    await state.update_data(
        text=message.text,
    )

    data = await state.get_data()
    await state.finish()

    data = {
        "prompt": data['text'],
        "n": 1,
        "size": "1024x1024"
    }

    await message.answer(GPTApi().images_api_post(data))


@dp.message_handler(text="Код")
async def start(message: Message):
    await message.answer("Введите любое сообщение", reply_markup=m_img)
    await CodeForm.text.set()


@dp.message_handler(state=CodeForm.text)
async def images_cmd(message: Message, state: FSMContext):
    await state.update_data(
        text=message.text,
    )

    data = await state.get_data()
    await state.finish()

    data = {
        "model": "text-curie-001",
        "prompt": data['text'],
        "temperature": 0,
        "max_tokens": 1024,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop": ["#", ";"]
    }

    await message.answer(GPTApi().code_api_post(data)['choices'][-1]['text'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
