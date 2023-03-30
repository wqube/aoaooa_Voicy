import json
import random
import time
from aiogram import types
from aiogram.types import ParseMode

from config import bot, dp
from aiogram.utils.markdown import hbold


# @dp.message_handler(commands="start")
async def start(message: types.Message):
    language_button_en = types.InlineKeyboardButton(text="En 🇬🇧", callback_data="en")
    language_button_ru = types.InlineKeyboardButton(text="Ru 🇷🇺", callback_data="ru")
    language_keyboard = types.InlineKeyboardMarkup(row_width=2).add(language_button_en, language_button_ru)

    user_id = message.from_user.id.__str__()

    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if user_id not in users_info:
        await message.answer(
            hbold("👋 Hello! Please, choose language!\n\n👋 Приветствую! Пожалуйста, выберете язык!"),
            reply_markup=language_keyboard,
            disable_notification=True)

    else:
        if users_info[str(user_id)]['language'] == "ru":
            await message.answer(
                hbold("Приветствую! 👋\n\nСкидывай мне голосовое сообщение, и я переведу его в текст, подробнее: /help"),
                disable_notification=True)
        elif users_info[str(user_id)]['language'] == "en":
            await message.answer(
                hbold("Greetings! 👋\n\nSend me a voice message and I'll translate it into text, more: /help"),
                disable_notification=True)


# @dp.callback_query_handlers(text="en")
async def callback_choose_language_en(callback: types.CallbackQuery):
    user_id = callback.from_user.id.__str__()

    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if user_id not in users_info:
        new_dict = {}
        new_dict[user_id] = {
            "is_admin": "False",
            "language": "en"
        }
        users_info.update(new_dict)

        with open("json_files/users.json", "w", encoding="utf-8") as file:
            json.dump(users_info, file, indent=4, ensure_ascii=False)

        await callback.message.answer(hbold(
            "You have successfully selected English language! 🇬🇧\n\nSend me a voice message and I'll translate it into text, more: /help"))
        await callback.answer()

    elif users_info[user_id]['language'] == 'ru':
        users_info[user_id]['language'] = "en"

        with open("json_files/users.json", "w", encoding="utf-8") as file:
            json.dump(users_info, file, indent=4, ensure_ascii=False)

        await callback.answer("You have successfully selected English language! 🇬🇧", show_alert=True)
    else:
        await callback.answer("❗ You have already chosen this language, please don't spam ❗", show_alert=True)


# @dp.callback_query_handlers(text="ru")
async def callback_choose_language_ru(callback: types.CallbackQuery):
    user_id = callback.from_user.id.__str__()

    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if user_id not in users_info:
        new_dict = {}
        new_dict[user_id] = {
            "is_admin": "False",
            "language": "ru"
        }
        users_info.update(new_dict)

        with open("json_files/users.json", "w", encoding="utf-8") as file:
            json.dump(users_info, file, indent=4, ensure_ascii=False)

        await callback.message.answer(hbold(
            "🇷🇺 Отлично, ты справился с выбором языка, на котором я буду с тобой общаться (его можно поменять в любой момент с помощью кнопки в меню)\n\nТеперь можешь скидывать мне голосовое сообщение, которое я переведу в текст, подробнее: /help"))
        await callback.answer()

    elif users_info[user_id]['language'] == 'en':
        users_info[user_id]['language'] = "ru"

        with open("json_files/users.json", "w", encoding="utf-8") as file:
            json.dump(users_info, file, indent=4, ensure_ascii=False)

        await callback.answer("Вы успешно выбрали русский язык! 🇷🇺", show_alert=True)
    else:
        await callback.answer("❗ Вы уже выбрали этот язык, пожалуйста, не спамьте ❗", show_alert=True)


# @dp.register_message_handler(commands="choose_language")
async def choose_language(message: types.Message):
    language_button_en = types.InlineKeyboardButton(text="En 🇬🇧", callback_data="en")
    language_button_ru = types.InlineKeyboardButton(text="Ru 🇷🇺", callback_data="ru")
    language_keyboard = types.InlineKeyboardMarkup(row_width=2).add(language_button_en, language_button_ru)

    await message.answer(
        hbold("👋 Hello! Please, choose language!\n\n👋 Приветствую! Пожалуйста, выберете язык!"),
        reply_markup=language_keyboard,
        disable_notification=True)


# @dp.message_handler(commands="help")
async def help(message: types.Message):
    user_id = message.from_user.id.__str__()
    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if users_info[user_id]['language'] == "ru":
        await bot.send_message(message.from_user.id,
            "*Приветик зайка 😘*\n\nВидимо, тебе нужно объяснение моей работы, ну так вот:\n\n"
            "Я бот, созданный для конвертирования голосовых сообщений в текст, проще говоря, если ваш не далёкий собеседник решит, что вам обязательно нужно послушать его обварожительный голосок (хе-хе), а вы не хотите портить свой прекрасный день голосом этого урода, то можете скидывать его голосовуху мне, я послушаю ее и почти сразу же выдам вам текст данного голосового сообщения\n\n*Приятного пользования! 💜*",
                               disable_notification=True, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(message.from_user.id,
            "*Hello! 👋*\n\nI am a bot designed to convert voice messages to text, just send it to me, and i will send you the text of this voice message\n\n*Enjoy using! 💜*",
                               disable_notification=True, parse_mode=ParseMode.MARKDOWN)


# @dp.message_handler()
async def all_messages(message: types.Message):
    o = ''
    mat = []
    che = []
    norm = []
    uwu = []

    with open("json_files/sticker_answer.json", encoding="utf-8") as file:
        sticker_answer = json.load(file)

    with open("json_files/cho.json", encoding="utf-8") as file:
        answer = json.load(file)

    with open("json_files/cenz.json", encoding="utf-8") as file:
        cenz_dict = json.load(file)

    for i in message.text.lower().split(" "):
        if i == "uwu":
            uwu.append(i)
        elif i in cenz_dict:
            mat.append(i)
        elif i in answer:
            o = i
            che.append(i)
        else:
            norm.append(i)

    if len(mat) >= 1:
        await bot.send_sticker(message.from_user.id, random.choice(sticker_answer))
    elif len(che) >= 1:
        await message.reply(f"ани{o} нормально общайся")
    elif len(uwu) >= 1:
        await bot.send_voice(message.from_user.id, open("uwu-voice.oga", "rb"))
    else:
        msg = await message.answer(
            "К сожалению я не смогла распознать Вашу команду😔.\nВоспользуйтесь кнопками или отправьте /help")
        time.sleep(3)
        await message.delete()
        await msg.delete()


def register_base_handlers(dp):
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(callback_choose_language_en, text="en")
    dp.register_callback_query_handler(callback_choose_language_ru, text="ru")
    dp.register_message_handler(help, commands="help")
    dp.register_message_handler(choose_language, commands="choose_language")
    dp.register_message_handler(all_messages)
