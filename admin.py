import json
import random
import time
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from config import bot, dp
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters.state import State, StatesGroup


@dp.message_handler(commands="admin")
async def admin_check(message: types.Message):
    user_id = message.from_user.id.__str__()

    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if users_info[user_id]['is_admin'] == "True":
        pass
    else:
        await message.answer("У вас нет прав админа")


class FSMstickers(StatesGroup):
    first_state = State()
    get_sticker = State()


@dp.message_handler(content_types=['sticker'], state=None)
async def scan_message_stickers(message: types.Message):
    user_id = message.from_user.id.__str__()

    with open("json_files/users.json", encoding="utf-8") as file:
        users_info = json.load(file)

    if users_info[user_id]['is_admin'] == "True":
        document_id = message.sticker.file_id
        file_info = await bot.get_file(document_id)
        f_id = file_info.file_unique_id.__str__()
        print(file_info.file_unique_id)
        # print(len(file_info))

        add_button = types.InlineKeyboardButton(text="✅", callback_data="add")
        delete = types.InlineKeyboardButton(text="❌", callback_data="delete_" + f_id)
        add_or_del_sticker = types.InlineKeyboardMarkup(row_width=2).add(add_button, delete)

        await message.answer(hbold("Добавить или удалить стикер?"), reply_markup=add_or_del_sticker)


        await FSMstickers.first_state.set()
        state = Dispatcher.get_current().current_state()

        async with state.proxy() as data:
            data["file_info"] = file_info

        await FSMstickers.get_sticker.set()

    else:
        pass



@dp.callback_query_handler(text_contains="add", state=FSMstickers.get_sticker)
async def add_sticker(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(data)
        await callback.message.answer_sticker(data)
    await state.finish()
    # file_info = callback.data[4:]
    # await callback.message.answer_sticker(file_info)

    # with open("json_files/sticker_answer.json", encoding="utf-8") as file:
    #     stickers = json.load(file)
    #
    # stickers.append(file_info.file_id)
    #
    # with open("json_files/sticker_answer.json", "w", encoding="utf-8") as file:
    #     json.dump(stickers, file, indent=4, ensure_ascii=False)


@dp.callback_query_handler(text_contains="delete_")
async def delete_sticker(callback: types.CallbackQuery):
    pass


def register_base_handlers(dp):
    dp.register_message_handler(admin_check, commands="admin")
    dp.register_callback_query_handler(add_sticker, text="add")
    dp.register_callback_query_handler(delete_sticker, text="delete")
