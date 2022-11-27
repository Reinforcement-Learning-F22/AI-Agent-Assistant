from aiogram import types
from aiogram.utils.callback_data import CallbackData

btn_cb = CallbackData("btn", "action", "message")


async def like_dislike_btn(msg: str):
    markup = types.InlineKeyboardMarkup()
    markup.insert(types.InlineKeyboardButton(text='Yes', callback_data=btn_cb.new(action='yes', message=msg)))
    markup.insert(types.InlineKeyboardButton(text='No', callback_data=btn_cb.new(action='no', message=msg)))
    return markup
