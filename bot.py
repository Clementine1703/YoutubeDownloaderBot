import asyncio
import logging
import sys
from os import getenv
import re


from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from downloader import Downloader

from statemanager import StateManager
from customexceptions import UrlException


TOKEN = '<token>'

dp = Dispatcher()
state_manager = StateManager()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    state_manager.set_active_keyboard('choosing_a_file_type')
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n\nЧто нужно скачать?", reply_markup=state_manager.get_active_keyboard())

@dp.message()
async def download_video(message: types.Message) -> None:
    if message.text == "Скачать видео":
        state_manager.set_active_keyboard('waiting_for_a_url')
        state_manager.set_active_format('.mp4')
        await message.answer('Введите URL видео', reply_markup=state_manager.get_active_keyboard())
    elif message.text == "Скачать аудиодорожку":
        state_manager.set_active_keyboard('waiting_for_a_url')
        state_manager.set_active_format('.mp3')
        await message.answer('Введите URL аудио', reply_markup=state_manager.get_active_keyboard())
    elif message.text.startswith('http'):

        try:
            match state_manager.get_active_format():
                case '.mp4':
                    path_to_file = Downloader.download_video(message.text)
                case '.mp3':
                    path_to_file = Downloader.download_audio(message.text)
        except UrlException as e:
            await message.answer(e.text)

        path_to_file = re.sub(r'\..{0,5}$', state_manager.get_active_format(), path_to_file) # Указываем необходимое расширение файла. (нужно для аудио файлов, т.к. мы используем постпроцессор, который переводит все аудиофайлы в mp3, но в переменной по прежнему остается старое расширение)
        
        file = FSInputFile(path_to_file)

        state_manager.set_active_keyboard('choosing_a_file_type')
        await message.reply_document(file, reply_markup=state_manager.get_active_keyboard())
    else:
        state_manager.set_active_keyboard('choosing_a_file_type')
        await message.answer(f"Что нужно скачать?", reply_markup=state_manager.get_active_keyboard())




async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())