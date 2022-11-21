from aiogram import types
from aiogram.utils.callback_data import CallbackData
from chatterbot import ChatBot
from loader import dp
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')
trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("chatterbot.corpus.english")
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)

btn_cb = CallbackData("btn", "action")
like_dislike_btn = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        types.InlineKeyboardButton(text='Yes', callback_data=btn_cb.new(action='yes')),
        types.InlineKeyboardButton(text='No', callback_data=btn_cb.new(action='no'))
    ]
])


@dp.message_handler(state=None, content_types=types.ContentTypes.TEXT)
async def bot_echo(message: types.Message):
    output_text = chatbot.get_response(message.text)
    await message.answer(text=str(output_text), reply_markup=like_dislike_btn)


@dp.callback_query_handler(btn_cb.filter())
async def action_cmd(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get('action')
    if action == 'like':
        await call.message.edit_text('You liked this message')
    elif action == 'dislike':
        await call.message.edit_text('You disliked this message')
