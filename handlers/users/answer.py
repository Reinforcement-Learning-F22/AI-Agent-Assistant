from aiogram import types
from chatterbot.trainers import ListTrainer

from loader import dp, chatbot


@dp.message_handler(lambda message: message.reply_to_message)
async def bot_echo(message: types.Message):
    answer = message.text
    question = message.reply_to_message.text
    trainer = ListTrainer(chatbot)
    trainer.train([question, answer])
    await message.answer(text='👍 Response added to bot!')
