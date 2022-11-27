from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from chatterbot import ChatBot

from config import load_config
from utils.database import MongoDB

config = load_config()
bot = Bot(token=config.bot.token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = MongoDB()
chatbot = ChatBot(
    name=config.bot.name,
    storage_adapter=config.bot.storage_adapter,
    logic_adapters=config.bot.logic_adapters,
    database_uri=db.url
)
