from aiogram import types
from chatterbot.conversation import Statement

from loader import dp, chatbot


# if message is replyed to bot message
@dp.message_handler(lambda message: message.reply_to_message)
async def bot_echo(message: types.Message):
    input_statement = Statement(text=message.reply_to_message.text)
    correct_response = Statement(text=message.text)
    chatbot.learn_response(correct_response, input_statement)
    await message.answer('Responses added to bot!')
