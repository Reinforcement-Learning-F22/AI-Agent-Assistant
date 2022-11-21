from loader import dp, db


@dp.message_handler()
async def test(message):
    await message.answer('test')
    info = await db.add_some_data()
    await message.answer(f"<code>{info}</code>")
