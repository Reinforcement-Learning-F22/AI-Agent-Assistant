from aiogram import types
from aiogram.utils.callback_data import CallbackData

btn_cb = CallbackData("btn", "action")
like_dislike_btn = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        types.InlineKeyboardButton(text='Yes', callback_data=btn_cb.new(action='yes')),
        types.InlineKeyboardButton(text='No', callback_data=btn_cb.new(action='no'))
    ]
])
