from aiogram import types

from loader import dp


@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    await message.answer('Help message')
