from loader import bot

from keyboards.inline import *
from loader import dp, chatbot, config, db

from chatterbot.conversation import Statement


@dp.message_handler(state=None, content_types=types.ContentTypes.TEXT)
async def bot_echo(message: types.Message):
    output_text = chatbot.get_response(message.text)
    text = f"<b>{str(output_text)}</b>\n\n<i>👋Hey, did you get the right answer to your question?</i>"
    db_message_id = await db.add_user_message(message.from_user.id, message.text)
    await message.answer(text=text, reply_markup=await like_dislike_btn(str(db_message_id.inserted_id)))


@dp.callback_query_handler(btn_cb.filter())
async def action_cmd(call: types.CallbackQuery, callback_data: dict):
    text = '😊 Thank you for your feedback!'
    if callback_data.get('action') == 'no':
        text += '\n🚀 I have already sent your question to the administrator.'
        user_message = await db.get_user_message(callback_data.get('message'))
        admin_text = f"<b>👤 User:</b> {call.from_user.full_name}\n\n" \
                     f"<b>📩 Message</b>: {user_message.get('message_text')}\n\n" \
                     f"<i>Awaiting an answer from the administrator👇</i>"
        await bot.send_message(chat_id=-815597083, text=admin_text)
        await bot.send_message(chat_id=-815597083, text=user_message.get('message_text'))
    await call.message.edit_text(text=text, reply_markup=None)
