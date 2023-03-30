import json
from aiogram import types
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
import admin
import base_handlers
import config
from config import bot, dp
import os
import subprocess
import uuid
import speech_recognition as sr
import requests
from aiogram import types


async def on_startup(_):
    await bot.set_my_commands([
        types.BotCommand("start", "Запуск бота | Start a bot 🔥"),
        types.BotCommand("help", "Как работает это чудо | How it work ❔"),
        types.BotCommand("choose_language", "Выбор языка | Choose a language 🇷🇺/🇬🇧"),
    ])
    # await bot.set_webhook(WEBHOOK_URL, drop_pending_updates = True)
    print("Слитая ботиха младшая онлайн\nhttps://t.me/aoaooa_3bot")


# async def on_shutdown(_):
#     await bot.delete_webhook()


base_handlers.register_base_handlers(dp)
admin.register_base_handlers(dp)


def recognizer(file_name_full_converted, language):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(file_name_full_converted) as mic:
            r.adjust_for_ambient_noise(source=mic, duration=0)
            audio = r.record(source=mic)
            query = r.recognize_google(audio_data=audio, language=language)

        # print(query)
        return query
    except sr.UnknownValueError:
        if language == "ru":
            return "Damn... Не поняла что ты сказал :/"
        else:
            return "Damn... I didn't understand what you said :/"


token = config.TOKEN


@dp.message_handler(content_types=['voice'])
async def voice_processing(message: types.Message):
    user_id = message.from_user.id.__str__()
    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if users_info[user_id]['language'] == "ru":
        bot_msg = await message.answer("Уже конвертирую... Подождите несколько секунд", disable_notification=True)
        language = 'ru'
    else:
        bot_msg = await message.answer("Converting already... Please wait a few seconds", disable_notification=True)
        language = 'en'

    filename = str(uuid.uuid4())
    file_name_full = f"./voice/{filename}.ogg"
    file_name_full_converted = "./ready/" + filename + ".wav"

    file_info = await bot.get_file(message.voice.file_id)
    print(token)
    print(file_info.file_path)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

    with open(file_name_full, 'wb') as f:
        f.write(file.content)

    process = subprocess.run(['ffmpeg', '-i', file_name_full, file_name_full_converted])

    if process.returncode != 0:
        raise Exception("Something went wrong")

    text = recognizer(file_name_full_converted, language)

    await bot_msg.delete()
    await message.reply(text, disable_notification=True)

    os.remove(file_name_full)
    os.remove(file_name_full_converted)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     skip_updates=True,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )
