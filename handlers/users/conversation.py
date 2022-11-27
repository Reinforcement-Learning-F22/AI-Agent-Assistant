from loader import bot

from keyboards.inline import *
from loader import dp, chatbot, config


@dp.message_handler(state=None, content_types=types.ContentTypes.TEXT)
async def bot_echo(message: types.Message):
    output_text = chatbot.get_response(message.text)
    await message.answer(text=str(output_text), reply_markup=like_dislike_btn)


@dp.callback_query_handler(btn_cb.filter())
async def action_cmd(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_text('Thank you for your feedback!')
    if callback_data.get('action') == 'no':
        await bot.send_message(chat_id=config.bot.admins[0], text=call.message.text)
